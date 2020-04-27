from wsc_html_parser import generate_df_from_html

def main():
    #Essa função gera um .json a partir do .html
    df = generate_df_from_html('portuguese_wsc.html')
    file = open('portuguese_wsc.json', 'w', encoding='utf-8')
    df.to_json(file, orient='records', force_ascii=False)
    file.close()

main()
