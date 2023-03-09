import streamlit as st
from reportlab.lib.pagesizes import A4 #A4 215x315
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm, cm
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from reportlab.lib import colors 
from reportlab.platypus import Image, Paragraph, Table
from reportlab.platypus.tables import Table
#from reportlab.plattypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY,  TA_LEFT
from tkinter.ttk import Style
import PDF_Images as PDF_I
import json
import os
from sympy import *



mesesDic = {
    "01":'enero',
    "02":'febrero',
    "03":'marzo',
    "04":'abril',
    "05":'mayo',
    "06":'junio',
    "07":'julio',
    "08":'agosto',
    "09":'septiembre',
    "10":'octubre',
    "11":'noviembre',
    "12":'diciembre'}
color_int = {
    "1":"#e0dcf4",
    "2":"#e0dcf4",
    "3":"#a0d4fc",
    "4":"#08fcfc",
    "5":"#00ff00",
    "6":"#ffff00",
    "7":"#ffaa00",
    "8":"#ff0000"
}

opt_map_ip = {
    "1":"#e0dcf4",
    "2":"#e0dcf4"
}
EMS_98 ={
    "1":"No sentido.",
    "2":"Sentido por muy pocas personas en reposo.",
    "3":"Sentido por pocas personas. Balanceo de objetos colgantes.",
    "4":"Sentido por muchas personas en el interior de edificaciones y por pocas en el exterior. Las ventanas, puertas y platos vibran.",
    "5":" Algunas personas se asustan y corren a la calle. Objetos pequeños se desplazan. Vaivén de puertas o ventanas. Leves grietas en casos aislados.",
    "6":"Algunas personas pierden el equilibrio. Algunos objetos caen. Muchas edificaciones presentan daños leves. ",
    "7":"Los muebles pesados se desplazan. Muchos edificios presentan grietas y caída de revestimiento de los muros.",
    "8":"Muchas personas tienen dificultad para mantenerse de pie. Caen objetos pesados. Las estructuras antiguas y débiles pueden colapsar.",
    "9":"Pánico general. Muchas construcciones débiles colapsan. Incluso los edificios ordinarios bien construidos muestran daños serios: fallas graves en los muros y fallas estructurales parciales.",
    "10":"Muchos edificios ordinarios bien construidos colapsan. ",
    "11":"La mayoría de los edificios ordinarios bien construidos colapsan, incluso algunos con buen diseño sismorresistente son destruidos.",
    "12":"Casi todos los edificios son destruidos."
}


width, height = A4

def perceived_intensity(ID_event):
    canv = canvas.Canvas("perceived_intensity_page.pdf", pagesize = A4)         #A4=210x297 mm
    folder="Events/"+ID_event    
    
    #Estilo parrrafos         
    normal_left = ParagraphStyle(name='Normal',alignment=TA_LEFT, fontSize=8)
    normal_justifiy = ParagraphStyle(name='Normal',alignment=TA_JUSTIFY, fontSize=8)        

    if  os.path.exists(folder+"/Data/"+f"inf_intpercibida_{ID_event}.json") == True:
        #Page3 
        #Intensidad percibida
        
        #Tabla, Datos
        with open(folder+"/Data/"+f"inf_intpercibida_{ID_event}.json","r") as json_file: 
            results_IP = json.load(json_file)    
        
        image_n_report = Image('PDF_Images/Numero_reportes1.png', 1.257*cm, 1*cm)
        image_centros = Image('PDF_Images/Centros_poblados.png', 1.1061*cm, 1*cm)
        image_muni = Image('PDF_Images/Municipios.png',1.138*cm, 1*cm)
        image_depart = Image('PDF_Images/Departamentos.png',1*cm, 1.294*cm)

        n_reportes = results_IP[0]["inf_intpercibida"][0]
        n_centros_poblados = results_IP[0]["inf_intpercibida"][1]
        n_municipio = results_IP[0]["inf_intpercibida"][2]
        n_departamentos = results_IP[0]["inf_intpercibida"][3]
        int_maxima = results_IP[0]["inf_intpercibida"][4]
        intensidad_reportada = results_IP[0]["inf_intpercibida"][5]
        centro_poblado_max = Paragraph(results_IP[0]["inf_intpercibida"][6], normal_justifiy)
        municipio_max = results_IP[0]["inf_intpercibida"][7]
        mun_rep_max = Paragraph(results_IP[0]["inf_intpercibida"][8][:-2],normal_justifiy)
        poblados_alejados_max = results_IP[0]["inf_intpercibida"][9]
        descripcion_ip = Paragraph( results_IP[0]["descr_im"],normal_justifiy )
        sent_otros_paises =  Paragraph(results_IP[0]["sent_otros_paises"],normal_justifiy )
        if sent_otros_paises:
            sent_otros_paises = Paragraph("No fue reportado como sentido en otros paises", normal_justifiy)        
        replicas_sentidas = Paragraph( results_IP[0]["replicas_sentidas"], normal_justifiy)
        if replicas_sentidas:
            replicas_sentidas = "Ninguna."
            
        revisado_ip ="Revisó: "+ results_IP[0]['quien_reviso'].strip(",")
        fuente_ip= "Fuente: "+results_IP[0]["inf_intpercibida"][10]

        Table_Data_pi= [["Número de reportes recibidos", n_reportes, image_n_report ],
                    [f"Sitios donde se reportó como \nsentido",f"provenientes de \n"+str(n_centros_poblados)+"\nCentros poblados",image_centros],
                    ["","ubicados en\n"+str(n_municipio)+"\nmunicipios",image_muni],
                    ["","de \n"+str(n_departamentos)+"\ndepartamentos",image_depart],
                    ["Intensidad máxima Reportada",f"{int_maxima}.  {intensidad_reportada}"],
                    [f"Centros poblados donde se \nreportó la intensidad máxima.", centro_poblado_max],
                    ["Descripción intensidad \nmáxima",Paragraph(EMS_98[str(int_maxima)],normal_justifiy )],
                    [f"Municipios con mayor \nnúmero de reportes.", mun_rep_max ],
                    [f"Centros poblados más alejados \ndel hipocentro donde fue \nreportado como sentido \nel sismo.", poblados_alejados_max[:-2]],
                    ["Sentido en otros países", sent_otros_paises],
                    [f"Réplicas reportadas \ncomo sentidas", replicas_sentidas ],
                    [fuente_ip],
                    [revisado_ip]]

        table_pi = Table(Table_Data_pi,colWidths=[4.2*cm, 3.6*cm],
                    rowHeights=[None, None, None , None,1*cm,1*cm, 2.5*cm, None, None, 1*cm, None, 0.5*cm, 0.5*cm])

        table_pi.setStyle([('GRID', (0,4), (-1,-3), 0.25, colors.green),
                    ('GRID', (0,0), (0,1), 0.25, colors.green),
                    ('BOX', (1,0), (-1,0), 0.25, colors.green),
                    ('BACKGROUND',(0,0),(0, -3),colors.darkgray),
                    ('BACKGROUND',(1,4),(1,4), HexColor(color_int[str(int_maxima)])),
                    ('VALIGN',(0,4),(-1,-1),'TOP'),
                    ('VALIGN',(0,0),(-1,2),'MIDDLE'),
                    ('VALIGN',(1,0),(1,-1),'TOP'),                
                    ('ALIGN',(1,0),(1,3),'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, -1),8),
                    ('FONTSIZE', (1, 0), (1, 0),20),
                    ('FONTSIZE', (1, 1), (1, 1),10),
                    ('FONTSIZE', (1, 2), (1, 2),10), 
                    ('FONTSIZE', (1, 3), (1, 3),10),                                 
                    ('SPAN',(0,1),(0,3)),
                    ('SPAN',(1,4),(-1,4)),
                    ('SPAN',(1,5),(-1,5)),
                    ('SPAN',(1,6),(-1,6)),
                    ('SPAN',(1,7),(-1,7)),
                    ('SPAN',(1,8),(-1,8)),
                    ('SPAN',(1,9),(-1,9)),
                    ('SPAN',(1,10),(-1,10)),
                    
                    ('BOX', (0,0), (-1,-1), 0.25, colors.green)])
                    
                    
        table_pi.wrapOn(canv, width, height)
        table_pi.drawOn(canv, 85*mm, 70*mm)   #posicion de la tabla
        styles = getSampleStyleSheet() 
        #Titulo mapa de intensidades
        canv.setFont('Helvetica', 7)
        canv.setFillColor(HexColor("#000000"))
        canv.drawString(25* mm, 235* mm, "Mapa de intensidades" )
        #Img mapa intensidad percibida
        Img_ip =ImageReader(f"{folder}/Images/map_int_perc_{ID_event}.png")
        #canv.drawImage(Img_ip, 5* mm, 100* mm, width = 75*mm,preserveAspectRatio=True, mask='auto')
        canv.drawImage(Img_ip, 6* mm, 119* mm, width = 75*mm,preserveAspectRatio=True, mask='auto')  ## Si el mapa el tomado del administrador de intensidades     
        #Img convenciones mapa intensidad percibida
        Img_c_ip =ImageReader(f"PDF_Images/leyenda_intensidad_persibida.png")
        canv.drawImage(Img_c_ip, 4* mm, 130* mm, width = 80*mm,preserveAspectRatio=True, mask='auto')
        #Img histograma intensidad percibida
        Img_ihp =ImageReader(f"{folder}/Images/histo_int_percibida_{ID_event}.png")        
        canv.drawImage(Img_ihp, 5* mm, 30* mm, width = 75*mm,preserveAspectRatio=True, mask='auto')
        #Leyenda epicentro
        Img_epicentro_pi =ImageReader("PDF_Images/Epicentro_leyenda.jpeg")
        canv.drawImage(Img_epicentro_pi, 5* mm, 132* mm, width = 20*mm,preserveAspectRatio=True, mask='auto')
    

    canv.save()
