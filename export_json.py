import json
import uuid

from django.core.management.base import BaseCommand
from gestoria.models import Familia


class Command(BaseCommand):
    help = "fills a json with all families"

    # def add_arguments(self, parser):
    #     parser.add_argument("file", type=str)

    def handle(self, *args, **options):
        data = []
        family_list = []
        for familia in Familia.objects.all():
            familia_uuid = str(uuid.uuid4())
            familia_dict = []
            for familiar in familia.primera_generacion.all():
                familiar_descendientes_dict = self.familiar_descendientes(familiar, familia_uuid)

                familia_dict.append(familiar_descendientes_dict)

            data.append(familia_dict)
            family_list.append(familia_uuid)

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        with open("family_list.json", "w", encoding="utf-8") as f:
            json.dump(family_list, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS("Export successful"))

    def familiar_descendientes(self, familiar, familia_uuid):
        familiar_dict = self.familiar_dict(familiar, familia_uuid)

        parejas = []
        for pareja in familiar.get_parejas():
            if pareja.primer_integrante == familiar:
                partner = pareja.segundo_integrante
            else:
                partner = pareja.primer_integrante

            pareja_dict = self.familiar_dict(partner, familia_uuid)

            if pareja.estado == "casados":
                pareja_dict["is_married"] = True
            else:
                pareja_dict["is_married"] = False

            hijos = []
            for hijo in pareja.hijos.all():
                hijos.append(self.familiar_descendientes(hijo, familia_uuid))
            pareja_dict["offspring"] = hijos

            parejas.append(pareja_dict)

        familiar_dict["partners"] = parejas

        return familiar_dict

    def familiar_dict(self, familiar, familia_uuid):
        nacimiento = None
        try:
            if familiar.partida_de_nacimiento and familiar.partida_de_nacimiento.fecha:
                nacimiento = familiar.partida_de_nacimiento.fecha.isoformat()
            elif familiar.fecha_de_nacimiento_desde:
                nacimiento = familiar.fecha_de_nacimiento_desde.isoformat()
        except:
            if familiar.fecha_de_nacimiento_desde:
                nacimiento = familiar.fecha_de_nacimiento_desde.isoformat()

        defuncion = None
        try:
            if familiar.partida_de_defuncion and familiar.partida_de_defuncion.fecha:
                defuncion = familiar.partida_de_defuncion.fecha.isoformat()
            elif familiar.fecha_de_defuncion_desde:
                defuncion = familiar.fecha_de_defuncion_desde.isoformat()
        except:
            if familiar.fecha_de_defuncion_desde:
                defuncion = familiar.fecha_de_defuncion_desde.isoformat()


        return {
            "sex": familiar.sexo,
            "birthday": nacimiento,
            "date_of_death": defuncion,
            "has_citizenship": "IT" in familiar.nacionalidades,
            "citizenship_resignation_date": None,
            "family_uuid": familia_uuid
        }
