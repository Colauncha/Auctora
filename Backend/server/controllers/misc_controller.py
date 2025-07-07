import httpx

from fastapi import Depends
from fastapi.routing import APIRouter
from server.config.app_configs import app_configs
from server.schemas import BanksQuery, APIResponse, ContactUsSchema
from server.middlewares.exception_handler import ExcRaiser400
from server.services.misc_service import ContactUsService


route = APIRouter(prefix='/misc', tags=['Miscellaneous'])


@route.post('/contact-us')
async def contact_us(
    data: ContactUsSchema
) -> APIResponse[str]:
    """
    Endpoint to handle contact us form submissions.
    """
    await ContactUsService.publish(data)
    return APIResponse(data="Your message has been Qeued!")


@route.get('/banks')
async def banks(query: BanksQuery = Depends()):
    paystack_url = f'{app_configs.paystack.PAYSTACK_URL}/bank'
    secret_key = app_configs.paystack.PAYSTACK_SECRET_KEY
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json"
    }
    param = query.model_dump()
    async with httpx.AsyncClient() as client:
        response = await client.get(paystack_url, headers=headers, params=param)
    if response.status_code != 200:
        raise ExcRaiser400(detail=response.json())
    return response.json()


@route.get('/states')
async def states() -> APIResponse[list]:
    states = [
        "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno", "Cross River", "Delta",
        "Ebonyi", "Edo", "Ekiti", "Enugu", "FCT", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi",
        "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto",
        "Taraba", "Yobe", "Zamfara"
    ]
    return APIResponse(data=states)


@route.get('/cities/{state}')
async def cities(state: str) -> APIResponse[list]:
    nigeria_states_cities = {
        "abia": [
            "Aba", "Umuahia", "Arochukwu", "Ohafia", "Bende", "Isiala Ngwa", "Osisioma Ngwa",
            "Ukwa East", "Ukwa West", "Ugwunagbo", "Ikwuano", "Isukwuato", "Umunneochi",
            "Obingwa", "Omumma", "Ntigha", "Abiriba", "Igbere", "Item", "Nkporo"
        ],
        "adamawa": [
            "Yola", "Mubi", "Jimeta", "Ganye", "Gombi", "Guyuk", "Hong", "Jada", "Lamurde",
            "Madagali", "Maiha", "Mayo Belwa", "Michika", "Toungo", "Fufore", "Demsa",
            "Shelleng", "Song", "Yelwa"
        ],
        "akwa ibom": [
            "Uyo", "Eket", "Ikot Ekpene", "Oron", "Abak", "Etinan", "Ikot Abasi", "Essien Udim",
            "Mkpat-Enin", "Onna", "Ukanafun", "Ibeno", "Mbo", "Eastern Obolo", "Ini",
            "Ika", "Urue-Offong/Oruko", "Udung Uko", "Nsit-Atai", "Nsit-Ibom", "Nsit-Ubium",
            "Okobo", "Oruk Anam"
        ],
        "anambra": [
            "Awka", "Onitsha", "Nnewi", "Aguata", "Ihiala", "Ekwulobia", "Ogidi", "Njikoka",
            "Idemili North", "Idemili South", "Oyi", "Anambra East", "Anambra West", "Ayamelum",
            "Dunukofia", "Orumba North", "Orumba South", "Ozubulu", "Umunze", "Agulu",
            "Adazi-Nnukwu", "Nnobi", "Nnewichi", "Obosi"
        ],
        "bauchi": [
            "Bauchi", "Azare", "Misau", "Gombe", "Katagum", "Jama'are", "Toro", "Gamawa",
            "Dass", "Tafawa Balewa", "Kirfi", "Alkaleri", "Itas/Gadau", "Giade", "Shira",
            "Zaki", "Dambam", "Bogoro", "Ningi", "Warji"
        ],
        "bayelsa": [
            "Yenagoa", "Brass", "Ogbia", "Sagbama", "Ekeremor", "Kolokuma/Opokuma", "Nembe",
            "Southern Ijaw"
        ],
        "benue": [
            "Makurdi", "Gboko", "Otukpo", "Katsina-Ala", "Adoka", "Agatu", "Apa", "Ado",
            "Buruku", "Guma", "Gwer East", "Gwer West", "Konshisha", "Kwande", "Logo",
            "Obi", "Ogbadibo", "Ohimini", "Oju", "Okpokwu", "Tarka", "Ukum", "Ushongo",
            "Vandeikya"
        ],
        "borno": [
            "Maiduguri", "Bama", "Dikwa", "Monguno", "Biu", "Askira/Uba", "Baga", "Damboa",
            "Gubio", "Guzamala", "Gwoza", "Hawul", "Jere", "Kala/Balge", "Konduga", "Kukawa",
            "Mafa", "Magumeri", "Marte", "Mobbar", "Ngala", "Nganzai", "Shani"
        ],
        "cross river": [
            "Calabar", "Ikom", "Ogoja", "Ugep", "Akamkpa", "Akpabuyo", "Bakassi", "Bekwarra",
            "Biase", "Boki", "Calabar Municipal", "Etung", "Obanliku", "Obubra", "Obudu",
            "Yakurr", "Yala"
        ],
        "delta": [
            "Asaba", "Warri", "Sapele", "Ughelli", "Agbor", "Burutu", "Kwale", "Ogwashi-Uku",
            "Oleh", "Ozoro", "Abraka", "Bomadi", "Eku", "Koko", "Oghara", "Patani", "Udu",
            "Uvwie", "Aniocha North", "Aniocha South", "Ethiope East", "Ethiope West",
            "Ika North East", "Ika South", "Isoko North", "Isoko South", "Ndokwa East",
            "Ndokwa West", "Okpe", "Oshimili North", "Oshimili South", "Sapele", "Ukwuani",
            "Warri North", "Warri South", "Warri South West"
        ],
        "ebonyi": [
            "Abakaliki", "Afikpo", "Onueke", "Edda", "Ezza North", "Ezza South", "Ikwo",
            "Ishielu", "Ivo", "Ohaozara", "Ohaukwu", "Onicha"
        ],
        "edo": [
            "Benin City", "Ekpoma", "Auchi", "Uromi", "Afuze", "Agenebode", "Ehor", "Igarra",
            "Igueben", "Irrua", "Sabongida-Ora", "Ubiaja", "Abudu", "Ewohimi", "Ibillo",
            "Idogbo", "Igieduma", "Iguobazuwa", "Ikpoba Okha", "Ogwashi-Uku", "Okenmwen",
            "Okpella", "Ugbowo", "Uhunmwonde"
        ],
        "ekiti": [
            "Ado-Ekiti", "Ikere", "Ijero", "Efon-Alaaye", "Aramoko-Ekiti", "Ido-Ekiti",
            "Igbara-Odo-Ekiti", "Ikole-Ekiti", "Ilawe-Ekiti", "Iyin-Ekiti", "Moba", "Oye-Ekiti",
            "Emure-Ekiti", "Gbonyin", "Ise-Orun", "Ekiti East"
        ],
        "enugu": [
            "Enugu", "Nsukka", "Awgu", "Oji River", "Achi", "Agbani", "Aninri", "Eha-Amufu",
            "Ezeagu", "Igbo-Etiti", "Igbo-Eze North", "Igbo-Eze South", "Isi-Uzo", "Udi",
            "Uzo-Uwani", "Nkanu East", "Nkanu West", "Enugu East", "Enugu North",
            "Enugu South"
        ],
        "gombe": [
            "Gombe", "Kumo", "Billiri", "Kaltungo", "Akko", "Balanga", "Deba", "Dukku",
            "Funakaye", "Kwami", "Nafada", "Shongom", "Yamaltu/Deba"
        ],
        "imo": [
            "Owerri", "Okigwe", "Orlu", "Mbaise", "Aboh Mbaise", "Ahiazu Mbaise", "Ehime Mbano",
            "Ezinihitte", "Ideato North", "Ideato South", "Ihitte/Uboma", "Ikeduru",
            "Isiala Mbano", "Isu", "Mbaitoli", "Ngor Okpala", "Njaba", "Nwangele",
            "Obowo", "Oguta", "Ohaji/Egbema", "Onuimo", "Orsu", "Oru East", "Oru West"
        ],
        "jigawa": [
            "Dutse", "Hadejia", "Gumel", "Birnin Kudu", "Babura", "Birniwa", "Buji", "Gagarawa",
            "Garki", "Gezawa", "Guri", "Gwaram", "Jahun", "Kafin Hausa", "Kaugama", "Kazaure",
            "Kiyawa", "Kiri Kasama", "Maigatari", "Malam Madori", "Miga", "Ringim", "Roni",
            "Sule Tankarkar", "Taura", "Yankwashi"
        ],
        "kaduna": [
            "Kaduna", "Zaria", "Kafanchan", "Soba", "Birnin Gwari", "Chikun", "Giwa", "Igabi",
            "Ikara", "Jaba", "Jema'a", "Kagarko", "Kajuru", "Kaura", "Kauru", "Kudan", "Lere",
            "Makarfi", "Sabon Gari", "Sanga", "Zango Kataf"
        ],
        "kano": [
            "Kano", "Kazaure", "Rano", "Gaya", "Ajingi", "Albasu", "Bagwai", "Bebeji", "Bichi",
            "Bunkure", "Dala", "Dambatta", "Dawakin Kudu", "Dawakin Tofa", "Doguwa", "Fagge",
            "Gabasawa", "Garko", "Garun Mallam", "Gezawa", "Gwale", "Gwarzo", "Kabo", "Karaye",
            "Kibiya", "Kiru", "Kumbotso", "Kunchi", "Kura", "Madobi", "Makoda", "Minjibir",
            "Nasarawa", "Rimin Gado", "Rogo", "Shanono", "Sumaila", "Takai", "Tarauni", "Tofa",
            "Tsanyawa", "Tudun Wada", "Ungogo", "Warawa", "Wudil"
        ],
        "katsina": [
            "Katsina", "Daura", "Funtua", "Malumfashi", "Bakori", "Batagarawa", "Batsari", "Baure",
            "Bindawa", "Charanchi", "Dandume", "Danja", "Dan Musa", "Dutsi", "Dutsin-Ma",
            "Ingawa", "Jibia", "Kaita", "Kankara", "Kankia", "Kurfi", "Kusada", "Mai'adua",
            "Mani", "Mashi", "Matazu", "Rimi", "Sabuwa", "Safana", "Zango"
        ],
        "kebbi": [
            "Birnin Kebbi", "Argungu", "Yauri", "Zuru", "Aleiro", "Arewa Dandi", "Augie",
            "Bagudo", "Bunza", "Dandi", "Fakai", "Gwandu", "Jega", "Kalgo", "Koko/Besse",
            "Maiyama", "Ngaski", "Sakaba", "Shanga", "Suru"
        ],
        "kogi": [
            "Lokoja", "Okene", "Kabba", "Idah", "Adavi", "Ajaokuta", "Ankpa", "Bassa", "Dekina",
            "Ibaji", "Igalamela-Odolu", "Ijumu", "Kogi", "Mopa-Muro", "Ofu", "Ogori/Magongo",
            "Okehi", "Yagba East", "Yagba West"
        ],
        "kwara": [
            "Ilorin", "Offa", "Jebba", "Kaiama", "Asa", "Baruten", "Edu", "Ilorin East",
            "Ilorin South", "Ilorin West", "Ifelodun", "Irepodun", "Isin", "Moro", "Oke Ero",
            "Oyun", "Pategi"
        ],
        "lagos": [
            "Ikeja", "Epe", "Badagry", "Agege", "Ajeromi-Ifelodun", "Alimosho", "Amuwo-Odofin",
            "Apapa", "Eti-Osa", "Ibeju-Lekki", "Ifako-Ijaiye", "Ikorodu", "Kosofe", "Lagos Island",
            "Mushin", "Ojo", "Oshodi-Isolo", "Somolu", "Surulere"
        ],
        "nasarawa": [
            "Lafia", "Akwanga", "Keffi", "Nasarawa", "Awe", "Doma", "Karu", "Kokona", "Obi",
            "Toto", "Wamba"
        ],
        "niger": [
            "Minna", "Suleja", "Kontagora", "Bida", "Agaie", "Agwara", "Borgu", "Bosso", "Chanchaga",
            "Edati", "Gbako", "Gurara", "Katcha", "Lapai", "Lavun", "Magama", "Mariga", "Mashegu",
            "Mokwa", "Munya", "Paikoro", "Rafi", "Rijau", "Shiroro", "Suleja", "Tafa", "Wushishi"
        ],
        "ogun": [
            "Abeokuta", "Ijebu-Ode", "Sagamu", "Ota", "Abeokuta North", "Abeokuta South",
            "Ado-Odo/Ota", "Egbado North", "Egbado South", "Ewekoro", "Ifo", "Ijebu East",
            "Ijebu North", "Ijebu North East", "Ikenne", "Imeko Afon", "Ipokia", "Obafemi Owode",
            "Odeda", "Odogbolu", "Remo North"
        ],
        "ondo": [
            "Akure", "Owo", "Ondo City", "Ikare", "Akoko North East", "Akoko North West",
            "Akoko South East", "Akoko South West", "Akure North", "Akure South", "Ese Odo",
            "Idanre", "Ifedore", "Ilaje", "Ile Oluji/Okeigbo", "Irele", "Odigbo", "Okitipupa",
            "Ondo East", "Ondo West", "Ose", "Owo"
        ],
        "osun": [
            "Osogbo", "Ile-Ife", "Ilesa", "Ede", "Atakunmosa East", "Atakunmosa West", "Ayedaade",
            "Ayedire", "Boluwaduro", "Boripe", "Ede North", "Ede South", "Egbedore", "Ejigbo",
            "Ifedayo", "Ifelodun", "Ife Central", "Ife East", "Ife North", "Ife South", "Ila",
            "Ilesa East", "Ilesa West", "Irepodun", "Irewole", "Isokan", "Iwo", "Obokun",
            "Odo Otin", "Ola Oluwa", "Olorunda", "Oriade", "Orolu"
        ],
        "oyo": [
            "Ibadan", "Ogbomoso", "Iseyin", "Oyo", "Afijio", "Akinyele", "Atiba", "Atisbo",
            "Egbeda", "Ibadan North", "Ibadan North East", "Ibadan North West", "Ibadan South East",
            "Ibadan South West", "Ibarapa Central", "Ibarapa East", "Ibarapa North", "Ido",
            "Irepo", "Iwajowa", "Kajola", "Lagelu", "Ogbomosho North", "Ogbomosho South",
            "Ogo Oluwa", "Olorunsogo", "Oluyole", "Ona Ara", "Orelope", "Ori Ire", "Saki East",
            "Saki West", "Surulere"
        ],
        "plateau": [
            "Jos", "Bukuru", "Pankshin", "Langtang", "Barkin Ladi", "Bassa", "Bokkos", "Jos East",
            "Jos North", "Jos South", "Kanam", "Kanke", "Langtang North", "Langtang South",
            "Mangu", "Mikang", "Pankshin", "Qua'an Pan", "Riyom", "Shendam", "Wase"
        ],
        "rivers": [
            "Port Harcourt", "Bonny", "Okrika", "Ahoada", "Abua/Odual", "Ahoada East",
            "Ahoada West", "Akuku-Toru", "Andoni", "Asari-Toru", "Degema", "Eleme", "Emuoha",
            "Etche", "Gokana", "Ikwerre", "Khana", "Obio/Akpor", "Ogba/Egbema/Ndoni", "Ogu/Bolo",
            "Omuma", "Opobo/Nkoro", "Oyigbo", "Tai"
        ],
        "sokoto": [
            "Sokoto", "Gwadabawa", "Illela", "Isa", "Kebbe", "Kware", "Rabah", "Sabon Birni",
            "Shagari", "Silame", "Tangaza", "Tureta", "Wamako", "Wurno", "Yabo"
        ],
        "taraba": [
            "Jalingo", "Wukari", "Gembu", "Bali", "Ardo Kola", "Donga", "Gashaka", "Gassol",
            "Ibi", "Jalingo", "Karim Lamido", "Kurmi", "Lau", "Sardauna", "Takum", "Ussa", "Yorro",
            "Zing"
        ],
        "yobe": [
            "Damaturu", "Potiskum", "Gashua", "Nguru", "Bade", "Bursari", "Damaturu", "Fika",
            "Fune", "Geidam", "Gujba", "Gulani", "Jakusko", "Karasuwa", "Machina", "Nangere",
            "Potiskum", "Tarmuwa", "Yunusari", "Yusufari"
        ],
        "zamfara": [
            "Gusau", "Kaura Namoda", "Tsafe", "Anka", "Bakura", "Bukkuyum", "Bungudu", "Gummi",
            "Gusau", "Kaura Namoda", "Maradun", "Maru", "Shinkafi", "Talata Mafara", "Zurmi"
        ],
        "fct": [
            "Abuja", "Gwagwalada", "Kubwa", "Kuje", "Abaji", "Bwari", "Gwagwalada", "Kwali"
        ]
    }
    return APIResponse(data=nigeria_states_cities.get(state.lower(), []))
