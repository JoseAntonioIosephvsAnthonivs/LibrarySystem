from PyQt5 import  uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

numero_id = 0

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Am@kus4shiro",
    database="cadastro_livros"
)
def editar_dados():#1
    global numero_id

    linha = segunda_tela.tableWidget.currentRow()

    cursor = banco.cursor(prepared=True) 
    cursor.execute("SELECT id FROM livros") #TABLE
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM livros WHERE id=" + str(valor_id))
    livro = cursor.fetchall()
    tela_editar.show()

    tela_editar.lineEdit.setText(str(livro[0][0]))
    tela_editar.lineEdit_2.setText(str(livro[0][1]))
    tela_editar.lineEdit_3.setText(str(livro[0][2]))
    tela_editar.lineEdit_4.setText(str(livro[0][3]))
    tela_editar.lineEdit_5.setText(str(livro[0][4]))
    tela_editar.lineEdit_6.setText(str(livro[0][5]))
    numero_id = valor_id

def salvar_dados_editados(): #2 salvar_valor_editado
    global numero_id

    autor = tela_editar.lineEdit_2.text() #2
    titulo = tela_editar.lineEdit_3.text()
    lancamento = tela_editar.lineEdit_4.text() #4
    resenha = tela_editar.lineEdit_5.text()
    categoria = tela_editar.lineEdit_6.text()
    cursor = banco.cursor(prepared=True)
    cursor.execute("UPDATE livros SET autor = '{}', titulo= '{}', lancamento = '{}', resenha= '{}', categoria= '{}' WHERE id = {}".format(autor, titulo, lancamento, resenha, categoria, numero_id))
    banco.commit()
    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()
    

def excluir_dados(): #3
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = banco.cursor(prepared=True) 
    cursor.execute("SELECT id FROM livros") #TABLE
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM livros WHERE id=" + str(valor_id))

def gerar_pdf(): #4
    cursor = banco.cursor(prepared=True)
    comando_SQL = "SELECT * FROM livros" # TABELA
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_livros.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200,800, "Livros cadastrados: ")
    pdf.setFont("Times-Bold", 18)
    
    pdf.drawString(10,750 , "ID") #0
    pdf.drawString(110,750 , "AUTOR") #1
    pdf.drawString(210,750 , "TÍTULO") #2
    pdf.drawString(310,750 , "LANÇAMENTO") #3
    pdf.drawString(410,750 , "RESENHA") #4
    pdf.drawString(510,750 , "CATEGORIA") #5

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 - y, str (dados_lidos[i][0]))
        pdf.drawString(110,750 - y, str (dados_lidos[i][1]))
        pdf.drawString(210,750 - y, str (dados_lidos[i][2]))
        pdf.drawString(310,750 - y, str (dados_lidos[i][3]))
        pdf.drawString(410,750 - y, str (dados_lidos[i][4]))
        pdf.drawString(510,750 - y, str (dados_lidos[i][5]))

    pdf.save()
    print("PDF gerado com sucesso!")

def funcao_principal():  #5
    # linha1 = formulario.lineEdit.text()
    linha2 = formulario.lineEdit_4.text() #2
    linha3 = formulario.lineEdit_3.text()
    linha4 = formulario.lineEdit_2.text() #4
    linha5 = formulario.lineEdit_5.text()

    categoria = ""

    if formulario.radioButton.isChecked() :
        print("Categoria Educacional foi selecionada.")
        categoria ="Educacional" #"Literatura"   
    elif formulario.radioButton_2.isChecked() :
        print("Categoria de Literatura foi selecionada.")
        categoria ="Literatura" #"Quadrinhos"   
    else:
        print("Categoria de Quadrinhos foi selecionada.")
        categoria ="Quadrinhos" #"Educacional"   


    # print("ID: ", linha1)
    print("Autor: ", linha2)
    print("Título: ", linha4)
    print("Lançamento: ", linha3)
    print("Resenha: ", linha5)

    cursor = banco.cursor(prepared=True)
    comando_SQL = "INSERT INTO livros (autor, titulo, lancamento, resenha, categoria) VALUES (%s,%s,%s,%s,%s)"
    dados = (str(linha2), str(linha4), str(linha3), str(linha5), categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()     # cursor.close()
    # formulario.lineEdit.setText("")
    formulario.lineEdit_4.setText("") #2
    formulario.lineEdit_3.setText("")
    formulario.lineEdit_2.setText("") #4
    formulario.lineEdit_5.setText("")

def chama_segunda_tela():
    segunda_tela.show()

    cursor = banco.cursor(prepared=True)
    comando_SQL = "SELECT * FROM livros" # TABELA
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(6)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 6):
            segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

app=QtWidgets.QApplication([])
formulario=uic.loadUi("formulario.ui")
segunda_tela=uic.loadUi("listar_dados.ui")
tela_editar=uic.loadUi("menu_editar.ui")
formulario.pushButton.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(gerar_pdf)
segunda_tela.pushButton_2.clicked.connect(excluir_dados)
segunda_tela.pushButton_3.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_dados_editados)


formulario.show()
app.exec()

# create table livros (
#     id INT NOT NULL AUTO_INCREMENT,
#     autor VARCHAR(50),
#     titulo VARCHAR(50),
#     lancamento VARCHAR(10),
#     resenha VARCHAR(50),
#     categoria VARCHAR(20),
#     PRIMARY KEY (id)
# );

# INSERT INTO livros (autor, titulo, lancamento, resenha, categoria) VALUES ("William Shakespeare","Macbeth",1603, "Livro trágico sobre ganância", "literatura")