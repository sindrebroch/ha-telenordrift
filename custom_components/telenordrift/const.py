"""Constants for the Pollenvarsel integration."""


from typing import Dict

from .models import Area

DOMAIN = "pollenvarsel"
CONF_AREA = "area"

AREA_PATH: Dict[Area, str] = {
    Area.TROMS: "50a10889-9132-402a-a14e-c98cd872bff3",
    Area.NORDLAND: "2680e4ac-1317-4423-baeb-b804e57c8285",
    Area.ROGALAND: "901f3d22-b95f-4b64-a181-0b847b76b1a3",
    Area.FINNMARK: "9a18de3a-06a3-4cb8-8eb0-9e42ed804ea4",
    Area.SØRLANDET: "fc1c3ec7-a311-4ce0-a5a7-b0e79813ecf7",
    Area.HORDALAND: "ed8a16e7-75aa-4994-b3b8-0a5b88c8f81e",
    Area.TRØNDELAG: "f2911165-bc25-494d-a331-42c05e14cfe2",
    Area.INDRE_ØSTLAND: "7c2de2d4-2ad0-45cb-bf25-10eeaf88c202",
    Area.MØRE_OG_ROMSDAL: "6ea90b97-547e-40ee-8eca-a2eb788ad567",
    Area.SOGN_OG_FJORDANE: "5d6f74b5-5e23-4271-ad85-b18452a7f849",
    Area.ØSTLANDET_MED_OSLO: "b5bb4856-2117-433d-bf18-53504ef2f101",
    Area.SENTRALE_FJELLSTRØK_I_SØR_NORGE: "a3d194c3-7788-45ae-82e7-e8be1d75a713",
}
