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
        # print('Successfully fetched data from the API.')
        try:
            data_fetched = response.json()
            data_fetched=data_fetched.get('items',[])
            # print('data_fetched:',data_fetched)
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

    url = f"https://connect.soligent.net/api/personalized/items?language=en&currency=USD&c=3510556&include=&sitepath=%2Fstore%2FsearchApi.ssp&country=US&use_pcv=F&fieldset=details&pricelevel=6&n=2&url={urlcomponent}&"

    payload = {}
    headers = {
    'Cookie': 'NLShopperId2=myhH-5s3AyBPMdqN; NLVisitorId=zfJENZs3AyRPMc7G; _ga=GA1.3.1454869050.1733743967; ajs_anonymous_id=%22d9da3a68-2755-4255-be92-223cf631d3ee%22; _hjSessionUser_3200933=eyJpZCI6IjQ5NTNiODAxLWNiNmUtNWFiZS1iZjEzLTBmZDVmOTk1NWYwOCIsImNyZWF0ZWQiOjE3MzM3NDM5NjcyODYsImV4aXN0aW5nIjp0cnVlfQ==; NS_VER=2024.2; _gid=GA1.3.97503205.1735196853; _gid=GA1.2.97503205.1735196853; chrole=1125:561244:cd4e3234; _hjSession_3200933=eyJpZCI6IjFhMmE0MTVkLWRmYWYtNGIzNC04Yjg1LWNlNTRkZTg3Nzk1YyIsImMiOjE3MzUyMDMxMjE0NDYsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; ak_bmsc=80C63B159C227BF7203C14A08E6AD7EB~000000000000000000000000000000~YAAQ7e/IF5MPIZuTAQAADg5DAho9WKYwk36Uqmy8MSCc3cxGJ46VOJbFvyvARSTschWBV2aCK8SoGx1K1aTdxorszSMQIzv6bt/7KmYBrhIDruUv+j88kCegvCJCI98r1/j2yVqR14Ad6peauY3SIY4UQwosnaNqi4La7WaccMyDrry3Jo6TxhM3C1aG1HUMyQBARNBxwNtw0Q7q2FH5+imRcxhwHiulMbTwONW70qNf3XOvzjMc2ooqmEd2zuRNBghC/aHNfgLI6hvfTB24tdTrS42ruq24Em+dVW2aVTFcuHUU0hyZ0tQctmibDU37I01tVuUN46l084qBE+fBLC/LwKTzOV6Q/qB97ogaygnZ4/EkY6cs1zINKFXhRO/LQT9aiDqcEjZVWnY1Yg==; JSESSIONID=sRwxlMK7qTC7FWVNEEQZeV5pQZWhJLhdjC0bSq92uxOhbw6cJHiX1R5lEyjVBrnbiLs0il1yvGkx-DqzHEagpJe-CaVWIda-SX_RM6n6tvmFfbLUnlkQauIGAGMCTnJx!1797622524; jsid_own=3510556.221014672; recentlyViewedIds=[105261%2C101457%2C105979%2C91307%2C61146]; _ga=GA1.2.1454869050.1733743967; _gat_gtag_UA_126763100_4=1; _gat_SCATracker=1; _iidt=8fqbAlPIGHQ+xIokGW0h+YukIO11+DYRdAzmz+IeXnKhPBUgIhQu8YKlZMGE8AAZ8RGf+uYo92uPitOxtOQ6axLvuU2APai3a/j1GbE=; _vid_t=w48qu2FM2Vc+QBzS6ofV58/AqA9HRAosUovVDcVKDLL2WbJy8jAnaLifMklQf23AWF4AY8F0i1htnEqX0lhfWfFiMEoUE8HiRce1p+A=; _ga_FSF2GJMBKC=GS1.1.1735204738.12.1.1735206969.0.0.0; SSPOperationId_e9fa9e30=32072c3d-9236-4933-8283-db241e8d8167; SSPOperationId_fafe38cc=4db88039-61e1-4eb1-8cb2-7ad7e9d31b59; bm_sv=0779DD4A1FC9145C576130B69833C69E~YAAQtV06F6daj7aTAQAAizFlAhp9Ge+Vg3W0aPILyXNadGEzquesh4KSKApzU+OsNVuvX2p4WP3dtWvundSiKXjfPoee/KISi7VSGkHJUxjCbMZpCKac0lhynf5xOw5Vdwi0zXngaViEd7dKaFNbybmky8O4gkAlkIQECoYhIJSTfWDOrGGSVN9B6VDq5c6pzbSb46ttuKg1MF4ZVtBJuZCVh0XPhbUn1islbyRoiNNJp1CEF8fzMJMiCQNIyMItFkE0Ow==~1; ak_bmsc=80C63B159C227BF7203C14A08E6AD7EB~000000000000000000000000000000~YAAQtV06Fxxkj7aTAQAA/TtmAho2qetSA49gSTN8eNu4vnV9pm9WavavZ78/3az407cJMkGNG9zarrW80MrccqAst84c2GfLYLmwmBgmf7zvmoFvtvpehQKISrqV7rYiaWu5A0bemQstDmTwkh/AWg2icf0lwUXDpkBImbe5ls/JKqHLiACZNua7aW6bTK3TzvYyOjFRM60/Dz3xqBgghIcOhYkhEevem4vuDl/L8Nv0aiynLQuRQJGbAiRef0ePvQafZt1Mgq/x3UVBhhWKz41TQJDDVl9n7l7IL+yNeuhyC3DiHGK/qgf7cD1duVlCyQmCWKkUuNCp2QDHrWKStPuw8K1ggcD2ybFSVqOweLEcdCogz7LZFloVBwMRGezi; bm_sv=0779DD4A1FC9145C576130B69833C69E~YAAQtV06Fx1kj7aTAQAA/TtmAhrArQgy/TA9lIhwDG+Q47zR3RGtf1Ua5KczcAhDOctKF8iGj1nb+klrF0i7r/HfPFt7zBGZ2GP3kih7+VNhpBzfL6rJ10WOb8i+xHgH1gCkJgi0XYjE/WGHG3HlgT6iM0DtWRy9U9+NwxKhRANUt3/EoTRmj067VvnlZYDw/pyNil9qmMSIpv3ymwn6HWQ5tCQ/fBqQVnVUpG2/lEaFH0uRMzRA9nalMBHJBUL1MBzKgw==~1; JSESSIONID=tY6VO4QeqTYVBrKRN-Qn02wHoNgT9ZAaOvHtPiN9DtrGVnSIZx7lZhcwVC-EUSW31TAukx1k4xJwxVC6g0Jn_t32HltRRVrsr9-jAU7hC7PuSCdf0hle2uKO0xemNZQ1!1797622524; NLSD3=tY6VO4QeqTYVBrKRN-Qn02wHoNgT9ZAaOvHtPiN9DtrGVnSIZx7lZhcwVC-EUSW31TAukx1k4xJwxVC6g0Jn_t32HltRRVrsr9-jAU7hC7PuSCdf0hle2uKO0xemNZQ1!1797622524; NLShopperId2=cbXsvN83A9Rl6Szg; NS_VER=2024.2; jsid_own=3510556.810399723'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.json())
    data=response.json()
    # print("data",data)
    for i in data.get('items',[]):
        # print(i)
        custitem_sol_sca_document_description=i.get('custitem_sol_sca_document_description','')
        document_description=extract_hrefs(custitem_sol_sca_document_description)
        # print(document_description)
        onlinecustomerprice_formatted=i.get('onlinecustomerprice_detail', {}).get('onlinecustomerprice', 0)
        onlinecustomerprice_formatted+=30
        onlinecustomerprice_formatted=str(onlinecustomerprice_formatted)
        weight=i.get('weight','')
        mpn=i.get('mpn','0')
        print('onlinecustomerprice_formatted:',onlinecustomerprice_formatted,type(onlinecustomerprice_formatted),' mpn:',mpn)
        
        weightunit=i.get('weightunit','')
        custitem_sol_length=i.get('custitem_sol_length','')
        custitem_sol_width=i.get('custitem_sol_width','')
        custitem_sol_height=i.get('custitem_sol_height','')
        dimentions=f'(L*W*H) {custitem_sol_length} X {custitem_sol_width} X {custitem_sol_height} inches'
        weight= f"{weight} {weightunit}"
    return dimentions,weight,document_description,mpn,onlinecustomerprice_formatted

def get_stocks_availability(data):
    import requests
    # print(data)
    url = f"https://connect.soligent.net/store_ss2/extensions/Soligent/InventoryDisplay/1.2.5/Modules/InventoryDisplay/SuiteScript2/CustomInvDisplay.Service.ss?c=3510556&itemid={data}&n=2"

    payload = {}
    headers = {
    'Cookie': 'ak_bmsc=7948BF870E85E3181F931C1CB5DB8922~000000000000000000000000000000~YAAQ9e/IFzH+UrSTAQAAyM6fARroXl7yZtQqUADZyoP+yl4jKI0eokG+8witX3sXv5eZJyGh08LiOAoF3dHiEF8nTycNN2H7TL+wxgSy+80EzX6aHL/FaFU+E+PPLWwB6d1n3D/DO4qzCMiAfVYqZo2yow/6gXn0CwV32k1OI5MN5Vni8YDAd3JF57egr6/a4g/wx4KxaTAfPwmrHiKU0ZA+GlhB0XyOw8eCa6KSYgvKFlIaVqoT1QTmB44blRdnzIY//QcACmjZg3KcKucxiyA5QWknLFQxJPb6R1frJxBDbyJGFUKzKopKDQkUWXLC1pfG0i4O4xVHeSdek5cDGD6uiK/JGsNhs9pBQEHw; bm_sv=228C636978CDE9FA897FFBA7109BDE59~YAAQb88uF+Jhu56TAQAAyDLrARorQaoTtBCdSp2s4s68xdVt5bgDzJAqVNbvItf/JYUBOOXqVy5D3Ouy+MQJsmfVklxM3rXz1Byz2gzhlsfZ77Tv/E9SDMN3ZDdBkgQxIfrtmtjDq2CDBOTuvLn6MqpVXIY8CdJgyJIJndWYIa4xhjKvs7JUyDb4aF/Tu+EQt0moN8kHS3I4C6XURp2v1IDBs1OR43tbpYFsUJt5gO4qJJagIbaROHleokKzNNS3nDw=~1; JSESSIONID=CzGLqDGvzGuyass5SMJfzRIXppJOlCwmZV4wLqTR-ctYNRjw3NI8kCELoVEELSGxEztPqTE3cQR7n2vH8mqxC1bz98G_0tVN2KMHOIY2GeLIkeRKrwjSnr0TzWrIJsZx!1797622524; NLSD3=CzGLqDGvzGuyass5SMJfzRIXppJOlCwmZV4wLqTR-ctYNRjw3NI8kCELoVEELSGxEztPqTE3cQR7n2vH8mqxC1bz98G_0tVN2KMHOIY2GeLIkeRKrwjSnr0TzWrIJsZx!1797622524; NLShopperId2=cbXsvN83A9Rl6Szg; NS_VER=2024.2; jsid_own=3510556.-531204213'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data=response.json()
    # print(data)
    return data



  
def process_data(data):
    if not data:
        logging.error("No data to process.")
        return
    final_data=[]
    warehouse=[
        {
            "internalid": 244,
            "label": "Arlington, TX"
        },
        {
            "internalid": 123,
            "label": "Fontana, CA"
        },
        {
            "internalid": 289,
            "label": "Fort Lauderdale, FL"
        },
        {
            "internalid": 187,
            "label": "Las Vegas, NV"
        },
        {
            "internalid": 285,
            "label": "Millstone, NJ"
        },
        {
            "internalid": 251,
            "label": "Orlando, FL"
        },
        {
            "internalid": 220,
            "label": "Sacramento, CA"
        },
        {
            "internalid": 278,
            "label": "Tampa, FL"
        }
    ]
    warehouse_dict = {f"{wh['internalid']}": wh['label'] for wh in warehouse}
    print(warehouse_dict,"warehouse_dict")
    if True:
        count=0 
        whare_house_names=[]
        for item in data:
            dimentions,weight,pdf_links,mpn,onlinecustomerprice_formatted=get_dimentions_pdf(item)
            stock_availabilty=get_stocks_availability(item.get('internalid', ''))
            # print(stock_availabilty['itemavailability'],'stock_availabilty')
            whare_house_names=[]
            for i in stock_availabilty['itemavailability']:
                # print(i['quantityavailable'],'quantityavailable')
                # print(i['name'],'name')
                # print(i['internalid'],'internalid')
                whare_house_name=warehouse_dict.get(i['internalid'],'N/A')
                print(whare_house_name,'whare_house_name--------------->')
                if whare_house_name == 'N/A' or whare_house_name.strip() == '' or i['quantityavailable'] == '':
                    print(whare_house_name,': ',f"--{i['quantityavailable']}--not availabble ")
                else:
                    print(whare_house_name,': ',f"--{i['quantityavailable']}--")
                    whare_house_names.append(f"{whare_house_name} : {i['quantityavailable']}")
                # print(whare_house_name,': ',i['quantityavailable'])
                # print("-"*50) 
            # print('dimentions : ',dimentions)
            # print('weight : ',weight)
            # print('pdf_links : ',pdf_links)
            count+=1
            manufacturer=item.get('manufacturer', 'N/A')
            # if mpn == 'JAM72D30-545/MB':
            #     print(item)
            #     break
            # print('manufacturer:',manufacturer)
            storedisplayname2=item.get('storedisplayname2', 'N/A')
            # print('storedisplayname2:',storedisplayname2)
            # onlinecustomerprice_formatted=item.get('onlinecustomerprice_detail', {}).get('onlinecustomerprice_formatted', 'N/A')
            # print(onlinecustomerprice_formatted)
            # print('onlinecustomerprice_formatted:',onlinecustomerprice_formatted,' mpn:',mpn)
            # onlinecustomerprice_formatted=f'{float(onlinecustomerprice_formatted[1:])+30}'
            # print('onlinecustomerprice_formatted:',onlinecustomerprice_formatted)
            # storedetaileddescription=rephrase_description(item.get('storedetaileddescription', 'N/A'))
            storedetaileddescription=item.get('storedetaileddescription', 'N/A')
            # print('storedetaileddescription:',storedetaileddescription)
            # salesdescription=rephrase_description(item.get('salesdescription', 'N/A'))
            salesdescription=item.get('salesdescription', 'N/A')
            # print('salesdescription:',salesdescription)
            isinstock=item.get('isinstock', 'N/A')
            # print('isinstock:',isinstock)
            mpn=mpn
            itemid=item.get('itemid', 'N/A')
            # print('itemid:',itemid)
            # itemimages_detail=item.get('itemimages_detail', {})
            # print('itemimages_detail:',itemimages_detail)
            # itemimages_detail=item.get('itemimages_detail', {}).get('1.default', {}).get('url', 'N/A')
            # if itemimages_detail == 'N/A':
            #     itemimages_detail=item.get('itemimages_detail', {}).get('urls', [])
            #     for i in itemimages_detail:
            #         itemimages_detail=i.get('url', 'N/A')
            # if itemimages_detail=={}:
            #     itemimages_detail='N/A'
            # print('itemimages_detail:',itemimages_detail)
            itemimages_detail = item.get('itemimages_detail', {})
            if 'urls' in itemimages_detail:
                # Extract only the URLs from the list of dictionaries under 'urls'
                urls = [url_info['url'] for url_info in itemimages_detail['urls'] if 'url' in url_info]
                itemimages_detail = urls if urls else 'N/A'  # List of URLs or 'N/A' if empty
            else:
                # Get the single URL from '1.default', or 'N/A' if not available
                itemimages_detail = itemimages_detail.get('1.default', {}).get('url', 'N/A')
                itemimages_detail=[itemimages_detail]
                    # print(f'-' * 50)
            # print(itemimages_detail,'itemimages_detail')  
              
            final_data.append({ "dimentions":dimentions, "whare_house_names":whare_house_names ,  "weight":weight,  "pdf_links":pdf_links,  "manufacturer":manufacturer,  "storedisplayname2":storedisplayname2,  "onlinecustomerprice_formatted":onlinecustomerprice_formatted, "storedetaileddescription":storedetaileddescription, "salesdescription":salesdescription, "isinstock":isinstock,"mpn":mpn, "itemid":itemid, "itemimages_detail":itemimages_detail,})
        return final_data
    # except KeyError as e:
    #     logging.error("Missing key in data: %s", e)
    # except Exception as e:
    #     logging.error("Unexpected error while processing data: %s", e)

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
    # print(total_item,'total_item----------->')
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
    solar_data = fetch_data()
      
    # print(solar_data,'solar_data')
     
    solar_data=process_data(solar_data)
      
    return solar_data

    # all_data=get_all_products()
    # all_data = all_data[:10]
    # all_data=process_data(all_data)
    # print(all_data)
    #return all_data


def add_products(data):
    # print('added sku :',data['itemid'])
    # print('added image :',data['itemimages_detail'])
    url = "https://demo.deepcomputerz.com/wp-json/wc/v3/products"
    imagedata=[]
    for image in data['itemimages_detail']:
        imagedata.append({
                    "src": image ,
                    "name": data['storedisplayname2'],
                    "alt": data['storedisplayname2']
                    })
    isinstock=data['isinstock']
    # print(imagedata,'imagedata')
    if isinstock==True:
        isinstock='instock'
        purchasable=True
    else:
        isinstock='outofstock'
        purchasable=False

    # print(isinstock,'isinstock')
    
    payload = json.dumps({
    "name": data['storedisplayname2'],
    "status": "publish",
    "catalog_visibility": "visible",
    "description": data['storedetaileddescription'],
    "short_description":  data['salesdescription'],
    "sku": data['mpn'],
    "price":data['onlinecustomerprice_formatted'] ,
    "regular_price":data['onlinecustomerprice_formatted'] ,
    "images": imagedata,
    "purchasable": purchasable,
   "categories": [
            {
                "id": 21,
                "name": "solar panel",
                "slug": "solar-panel"
            }
        ],
    # "attributes": [
    #     {
            
    #         "name": "MPN",
    #         "slug": "pa_mpn",
    #         "position": 0,
    #         "visible": True,
    #         "variation": False,
    #         "options": [
    #             data['mpn']
    #         ]
    #     }
    # ],
     "attributes": [
            {
                "id": 1,
                "name": "product availvality",
                "slug": "pa_product-availvality",
                "position": 0,
                "visible": True,
                "variation": False,
                "options": data['whare_house_names']
            }
        ],
    "stock_status": isinstock
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic Y2tfOTczMzY2NzBhOWMzYjA4YmFhZjU4ZDZkMTdmNzJlMWYxM2EzYTdkYjpjc18wNmM1MTY1NmEzYjc3ZTJiMzJhYjlmOTYxZmZkYWM3MmFiYTQwNDdl'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

def update_wp_product(data,id):
    # print('updated sku :',data['itemid'])
    # print('updated image :',data['itemimages_detail'])
    # print('updated id :',id)
    
    url = f"https://demo.deepcomputerz.com/wp-json/wc/v3/products/{id}"
    imagedata=[]
    for image in data['itemimages_detail']:
        imagedata.append({
                    "src": image ,
                    "name": data['storedisplayname2'],
                    "alt": data['storedisplayname2']
                    })
    isinstock=data['isinstock']
    # print(imagedata,'imagedata')
    if isinstock==True:
        isinstock='instock'
        purchasable=True
    else:
        isinstock='outofstock'
        purchasable=False
    print(data["whare_house_names"])
    payload = json.dumps({
    "name": data['storedisplayname2'],
    "status": "publish",
    "catalog_visibility": "visible",
    "description": data['storedetaileddescription'],
    "short_description":  data['salesdescription'],
    "sku": data['mpn'],
    "price":data['onlinecustomerprice_formatted'] ,
    "regular_price":data['onlinecustomerprice_formatted'] ,
    "images": imagedata,
    "weight": data['weight'] ,
        
    "categories": [
            {
                "id": 21,
                "name": "solar panel",
                "slug": "solar-panel"
            }
        ],
    "purchasable": purchasable,
    "stock_status": isinstock,
    # "attributes": [
    #     {
    #         "id": 2,
    #         "name": "MPN",
    #         "slug": "pa_mpn",
    #         "position": 0,
    #         "visible": True,
    #         "variation": False,
    #         "options": [
    #             data['mpn']
    #         ]
    #     }
    # ],
    "attributes": [
            {
                "id": 1,
                "name": "product availvality",
                "slug": "pa_product-availvality",
                "position": 0,
                "visible": True,
                "variation": False,
                "options": data['whare_house_names']
            },
            {
                "id": 2,
                "name": "Dimensions (LxWxH):",
                "slug": "pa_dimensions-lxwxh",
                "position": 1,
                "visible": True,
                "variation": True,
                "options": [
                    data["dimentions"]
                ]
            }
        ],
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic Y2tfOTczMzY2NzBhOWMzYjA4YmFhZjU4ZDZkMTdmNzJlMWYxM2EzYTdkYjpjc18wNmM1MTY1NmEzYjc3ZTJiMzJhYjlmOTYxZmZkYWM3MmFiYTQwNDdl'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print('Updated Product',response.text)


   
# def get_data_from_wp():
#     url = "https://demo.deepcomputerz.com/wp-json/wc/v3/products"
#     payload = {}
#     headers = {
#     'Authorization': 'Basic Y2tfOTczMzY2NzBhOWMzYjA4YmFhZjU4ZDZkMTdmNzJlMWYxM2EzYTdkYjpjc18wNmM1MTY1NmEzYjc3ZTJiMzJhYjlmOTYxZmZkYWM3MmFiYTQwNDdl'
#     }
#     response = requests.request("GET", url, headers=headers, data=payload)
#     skus=[]
#     ids=[]
#     for i in response.json():
#         skus.append(i.get('sku',''))
#         ids.append(i.get('id',''))
#     return skus,ids
def get_data_from_wp():
    base_url = "https://demo.deepcomputerz.com/wp-json/wc/v3/products"
    auth_header = 'Basic Y2tfOTczMzY2NzBhOWMzYjA4YmFhZjU4ZDZkMTdmNzJlMWYxM2EzYTdkYjpjc18wNmM1MTY1NmEzYjc3ZTJiMzJhYjlmOTYxZmZkYWM3MmFiYTQwNDdl'
    skus = []
    ids = []
    page = 1

    while True:
        url = f"{base_url}?per_page=100&page={page}"
        headers = {
            'Authorization': auth_header
        }
        response = requests.get(url, headers=headers)
        products = response.json()

        # Check if the response contains any products
        if not products or response.status_code != 200:
            break

        for product in products:
            skus.append(product.get('sku', ''))
            ids.append(product.get('id', ''))

        page += 1

    return skus, ids

def sync_products(wp_sku,ids,data):
    for products in data:
        # print(products['mpn'] in wp_sku,products['mpn'],wp_sku)
        if products['mpn'] in wp_sku:
            id=ids[wp_sku.index(products['mpn'])]
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
