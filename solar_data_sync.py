import requests
import logging
import sys
import openai
from bs4 import BeautifulSoup
import requests
import json
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_fetch.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

 
# Set up your OpenAI API key
openai.api_key = ""

def rephrase_description(description):
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that rephrases text.Do not add more text"},
                {"role": "user", "content": f"Rephrase this: {description}"}
            ],
            max_tokens=150
        )
        rephrased_text = response['choices'][0]['message']['content'].strip()
        return rephrased_text
    except Exception as e:
        logging.error(f"Error in rephrasing the description: {e}")
        return description

def fetch_data():
    url = r"https://connect.soligent.net/api/cacheable/items?c=3510556&commercecategoryurl=%2Fpv&country=US&currency=USD&fieldset=search&include=facets&language=en&limit=100&n=1&offset=0&pricelevel=5&sort=custitem_ns_sc_ext_ts_90_amount%3Adesc&use_pcv=F"

    headers = {
        'Cookie': r'ak_bmsc=76EA706638B21609425957B0F525A23B~000000000000000000000000000000~YAAQL7YRYOx1OpqTAQAAmGaitRoFXRQUnBHp0rzhD0UGuvBW8zoKtMA6pkDrny/kYv+SNiNRqSt1ajhomcIt8GsZgUr38lQ3qM3v2KoDo/4jW8CrF3qT9VS4nLF+G5/YHfZzlEr5XjXASFsp/NeG7shUz+G/L2YR27Z+RCIV4YewfJzGJIrXZt3a442K7IyL36CuMI2gdMRUyarpXF3koFl58SjnyqyDoKDhjXgkCDF4vVUp+ihi67EFxfb0k7WXrp6p0RzeIrMZvkJ5CA6GpxXLJJ/hl3NbG58pFXOSHHwTzeC8qAsOVMRfE0uZZjGCSpQiur5HiiwPl11VplkA/9uhzOW3hn0eg176aUHf; bm_sv=4C266B8BBB4C93155C42FC354A0FD1E4~YAAQJ7YRYJz4q7OTAQAA09amtRorFkrCsUT7G6/Jiij6eDv3ruVuing06qBYZSOnt4KWkfXBVBi7wRSeqWJuykHTBQECmdlyE35DUUiRBnCopPpU+5ZLknyWDQdBo1Y0nS4Bw0xuOIBhJLiMoc6RysewQWXnTneckuU/MXUUBpBfNI+mDPaQyqPGWDqjUMa7xbYHQlesv9JR0cj0dGv1SoaGqPKitmznyjAf0XtgjP3C4YHzZmyfS5lCEpBh/WAxeNQ=~1'
    }

    try:
        logging.info("Sending GET request to the API.")
        response = requests.get(url, headers=headers)

        # Check for HTTP errors
        response.raise_for_status()

        logging.info("Successfully fetched data from the API.")

        try:
            data_fetched = response.json()
            data_fetched=data_fetched.get('items',[])
            logging.info("Successfully parsed JSON response.")
            return data_fetched
        except ValueError as e:
            logging.error("Error parsing JSON response: %s", e)
            return None

    except requests.exceptions.RequestException as e:
        logging.error("Error during API request: %s", e)
        return None

def extract_hrefs(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract all href attributes from anchor tags
    hrefs = [f"https://connect.soligent.net{a['href']}" for a in soup.find_all('a', href=True)]
    return hrefs

def get_dimentions_pdf(data):
    urlcomponent=data.get('urlcomponent','')

    url = f"https://connect.soligent.net/api/cacheable/items?c=3510554566456&country=US&currency=USD&fieldset=details&include=&language=en&n=2&pricelevel=5&url={urlcomponent}&use_pcv=F"

    payload = {}
    headers = {
    'Cookie': 'ak_bmsc=F87AE0E3A11F8D4C65AC294FA35FC93D~000000000000000000000000000000~YAAQJ7YRYPnRQ7STAQAApVFc2BrrTkadNnoYIw7JVxBgHI/MurKQ6IX10EsD3KfYyKJH3rmH2eHH585P9nhEqdD9ry90Kxhne+3fRk5XN5jKRlJJlbzwfuQudjnM8GyyH3HmQklht1zfoNcN7kBZfr1nqVcNr5WLQvUkm3o4Khxp7nLz9IUm5rxgvvnbB8u3Lj7uGOZDmaXRYv1qKRoMpAtylfq/ivGDxBv6542rX5y9d2w0PcLDueWi4CKGYZ1PJIKG9+nhkezA6uz1pU2tzwHarCx9TAM0tpRMoJktcJbKYi+rkDqUA8kMwakxYwqdst3PHEbBU3aZ8NyPjvX+lqMt26fY1wqP+CJN+Myz; bm_sv=8B569CF1147CB291B209FCD452F28E37~YAAQlAVaaF7VXM6TAQAAEDpi2BrP2lAbcyfYyiA7NvGhYiT9cXdA09YBZDJSmADOhnC+njcKzFHKzk6aNl0jRX0Q+1VvpS+hwZb+sGLwN5mLsLsegRM9gP2ERBFmJUDLstyPyhkDw7Ii4GFRILw24ACIZpzLhp/mZMU2b9MAupY5NmdJlpGE4MhcwBv4u4wbrq6N6xNdfC6oG7JNbdIkoyqLFlzl/thRUEa0EIlg1Lrc1Cto0o1IFJp0Y72m/+62niV9~1'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.json())
    data=response.json()
    for i in data.get('items',[]):
        
        custitem_sol_sca_document_description=i.get('custitem_sol_sca_document_description','')
        document_description=extract_hrefs(custitem_sol_sca_document_description)
        # print(document_description)
        weight=i.get('weight','')
        weightunit=i.get('weightunit','')
        custitem_sol_length=i.get('custitem_sol_length','')
        custitem_sol_width=i.get('custitem_sol_width','')
        custitem_sol_height=i.get('custitem_sol_height','')
        dimentions=f'(L*W*H) {custitem_sol_length} X {custitem_sol_width} X {custitem_sol_height} inches'
        weight= f"{weight} {weightunit}"
    return dimentions,weight,document_description
   
def process_data(data):
    if not data:
        logging.error("No data to process.")
        return
    final_data=[]
    try:
        count=0
        for item in data:
            dimentions,weight,pdf_links=get_dimentions_pdf(item)
            
            # print('dimentions : ',dimentions)
            # print('weight : ',weight)
            # print('pdf_links : ',pdf_links)
            count+=1
            manufacturer=item.get('manufacturer', 'N/A')
            
            # print('manufacturer:',manufacturer)
            storedisplayname2=item.get('storedisplayname2', 'N/A')
            # print('storedisplayname2:',storedisplayname2)
            onlinecustomerprice_formatted=item.get('onlinecustomerprice_formatted', 'N/A')
            # print('onlinecustomerprice_formatted:',onlinecustomerprice_formatted)
            # storedetaileddescription=rephrase_description(item.get('storedetaileddescription', 'N/A'))
            storedetaileddescription=item.get('storedetaileddescription', 'N/A')
            # print('storedetaileddescription:',storedetaileddescription)
            # salesdescription=rephrase_description(item.get('salesdescription', 'N/A'))
            salesdescription=item.get('salesdescription', 'N/A')
            # print('salesdescription:',salesdescription)
            isinstock=item.get('isinstock', 'N/A')
            # print('isinstock:',isinstock)
            itemid=item.get('itemid', 'N/A')
            # print('itemid:',itemid)
            itemimages_detail=item.get('itemimages_detail', {}).get('1.default', {}).get('url', 'N/A')
            if itemimages_detail == 'N/A':
                itemimages_detail=item.get('itemimages_detail', {}).get('urls', [])
                for i in itemimages_detail:
                    itemimages_detail=i.get('url', 'N/A')
            if itemimages_detail=={}:
                itemimages_detail='N/A'
            # print('itemimages_detail:',itemimages_detail)
                      
            # print(f'-' * 50)
            final_data.append({ "dimentions":dimentions,  "weight":weight,  "pdf_links":pdf_links,  "manufacturer":manufacturer,  "storedisplayname2":storedisplayname2,  "onlinecustomerprice_formatted":onlinecustomerprice_formatted, "storedetaileddescription":storedetaileddescription, "salesdescription":salesdescription, "isinstock":isinstock, "itemid":itemid, "itemimages_detail":itemimages_detail,})
        return final_data
    except KeyError as e:
        logging.error("Missing key in data: %s", e)
    except Exception as e:
        logging.error("Unexpected error while processing data: %s", e)

def get_all_products():
    

    url = "https://connect.soligent.net/api/cacheable/items?c=3510556&country=US&currency=USD&fieldset=search&include=facets&language=en&limit=2&n=2&offset=0&pricelevel=1&use_pcv=F"

    payload = {}
    headers = {
    'Cookie': 'ak_bmsc=96AC6ABBC2EDBC3144B58569032D082A~000000000000000000000000000000~YAAQL7YRYKMf4ZqTAQAAATEnzxrwhLSHmv4FNhj9r9DiYRQ/Wz1hk3dPasvScI8omtNMsiW9ZFMF3Spmx3yW3zWLnWf4cxkpejNmED8NifPqUKNYdqRZk3+S38T7VTkJH3Y9hbx+5ZjcDEs+FXW9R15XE/fptgvF2Wt/w3G/AJ6zJ/ODUDf99/pwrkEzPgCYkEz/ikSPILsvNXUKopzsceu39CJdq6zz0ulWj1BGcetk1yH23zWD7mwM1afq91PzmGxNVtG3ihSD8D52bjsvMiHAglB3tuyqQdI6xFMx4VbzOxIcyZChAazxG3ihvVCJQQtD83QM2heI8hlXN5jMXFcTYAmstlrClhHOKkrn; bm_sv=4782A60BB3C526864854A2C1D98DED31~YAAQbV06F4cP0pqTAQAAdlczzxpSOO3W38BUVZE3ZpjTPZWSQIXv4WM+rOFf+66GapOqrNI1G9Jvcz8vztRSGRfoMuwd/ukVIEGXHfrQIIuqL9rJc4nKClxQC489e/g++36IyFBiNkerGfxT14fJkg3jZJk/xqlwhVBpcDLBu4J7MVUOBZOuICJclJKU9Q2AdHrnuGmb4rTSE/6p432T0R1DgLfoS46tR8cK7KSqodUmhnxDsK5faoIlPkwBIqu/yhVx~1'
    }

    total_item = requests.request("GET", url, headers=headers, data=payload)
    total_item=total_item.json()
    total_item=total_item.get('total',0)
    
    total_item=int(total_item)
    print(total_item,'total_item----------->')
    items=[]
    def fetch_data(offset):
        url = rf"https://connect.soligent.net/api/cacheable/items?c=3510556&country=US&currency=USD&fieldset=search&include=facets&language=en&limit=100&n=2&offset={offset}&pricelevel=1&use_pcv=F"
        response = requests.get(url, headers=headers, data=payload)
        data = response.json()
        return data.get('items', [])

    # Use map to fetch data for each offset
    offsets = range(0, total_item, 100)
    items = sum(map(fetch_data, offsets), [])
      
    return items

def get_data_from_distrubuters():
    # solar_data = fetch_data()
    # solar_data=process_data(solar_data)
    all_data=get_all_products()
    all_data=process_data(all_data)
    return all_data


def add_products(data):
    print('added sku :',data['itemid'])
    print('added image :',data['itemimages_detail'])
    url = "https://demo.deepcomputerz.com/wp-json/wc/v3/products"
    payload = json.dumps({
    "name": data['storedisplayname2'],
    "status": "publish",
    "catalog_visibility": "visible",
    "description": data['storedetaileddescription'],
    "short_description":  data['salesdescription'],
    "sku": data['itemid'],
    "price":data['onlinecustomerprice_formatted'] ,
    "regular_price":data['onlinecustomerprice_formatted'] ,
    "images": [
        {
        "src": data['itemimages_detail'],
        "name": "shock absorber",
        "alt": ""
        }
    ],
    "stock_status": "instock"
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic Y2tfOTczMzY2NzBhOWMzYjA4YmFhZjU4ZDZkMTdmNzJlMWYxM2EzYTdkYjpjc18wNmM1MTY1NmEzYjc3ZTJiMzJhYjlmOTYxZmZkYWM3MmFiYTQwNDdl'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

def update_wp_product(data,id):
    print('updated sku :',data['itemid'])
    print('updated image :',data['itemimages_detail'])
    print('updated id :',id)
    
    url = f"https://demo.deepcomputerz.com/wp-json/wc/v3/products/{id}"
    payload = json.dumps({
    "name": data['storedisplayname2'],
    "status": "publish",
    "catalog_visibility": "visible",
    "description": data['storedetaileddescription'],
    "short_description":  data['salesdescription'],
    "sku": data['itemid'],
    "price":data['onlinecustomerprice_formatted'] ,
    "regular_price":data['onlinecustomerprice_formatted'] ,
    "images": [
        {
        "src": data['itemimages_detail'],
        "name": "shock absorber",
        "alt": ""
        }
    ],
    "stock_status": "instock"
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic Y2tfOTczMzY2NzBhOWMzYjA4YmFhZjU4ZDZkMTdmNzJlMWYxM2EzYTdkYjpjc18wNmM1MTY1NmEzYjc3ZTJiMzJhYjlmOTYxZmZkYWM3MmFiYTQwNDdl'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    # print(response.text)


   
def get_data_from_wp():
    url = "https://demo.deepcomputerz.com/wp-json/wc/v3/products"
    payload = {}
    headers = {
    'Authorization': 'Basic Y2tfOTczMzY2NzBhOWMzYjA4YmFhZjU4ZDZkMTdmNzJlMWYxM2EzYTdkYjpjc18wNmM1MTY1NmEzYjc3ZTJiMzJhYjlmOTYxZmZkYWM3MmFiYTQwNDdl'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    skus=[]
    ids=[]
    for i in response.json():
        skus.append(i.get('sku',''))
        ids.append(i.get('id',''))
    return skus,ids


def sync_products(wp_sku,ids,data):
    for products in data:
        if products['itemid'] in wp_sku:
            id=ids[wp_sku.index(products['itemid'])]
            update_wp_product(products,id)
        else:
            add_products(products)
            








def main():
    logging.info("Starting data fetch and process script.")
    data_from_distrubuters=get_data_from_distrubuters()
    
    sku_from_wp,id_from_wp=get_data_from_wp()
    
    sync_products(sku_from_wp,id_from_wp,data_from_distrubuters)
    logging.info("Script completed.")




if __name__ == "__main__":
    main()
