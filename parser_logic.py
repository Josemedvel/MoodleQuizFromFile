from icecream import ic

def readFile(file_name):
    extracted_questions = []
    result = []
    with open(
        file_name,
        "r",
        encoding="UTF8",
    ) as file:
        question_blocks = file.read().split("\n\n") 
        extracted_questions = [q for q in question_blocks if q != ""]  # filtro de preguntas vacías
        cleaned_questions = [] #preguntas sin líneas vacías
        
        # print(extracted_questions)
        for q in extracted_questions: # limpiar lineas vacías en las preguntas 
            cleaned_questions.append(q.strip())

        for q in cleaned_questions:
            q_lines = q.split("\n")
            first_line = q_lines[0].split("|")
            # print(first_line)
            punt = 1
            pen = float(punt) / (len(q_lines) - 1)  # 1 sola línea en el caso de que no esté especificada la puntuación y penalización
            # falta implementar penalización media
            if (
                len(first_line) == 2
            ):  # si está especificada la puntuación y penalización
                punt = float(first_line[0])
                pen = float(punt) / (len(q_lines) - 2)
            # print(punt,pen)
            result.append(
                {
                    "puntuation": punt,
                    "penalization": pen,
                    "question": q_lines[1:] if len(first_line) == 2 else q_lines,
                }
            )
    return result
def writeFile(file_content, name):
    with open(name,'w',encoding='UTF8') as new_file:
        new_file.write(file_content)
def parseCorrectWrong(question):
    ic(question)
    result = {
        'wrong': [],
        'correct': []
        }
    for answ in question[1:]:
        if answ.startswith('-'):
            result['wrong'].append(answ[1:])
        else:
            result['correct'].append(answ[1:])
    if len(result['correct']) > 1 or len(result['correct']) == 0:
        raise Exception('No está pensado el programa para tener más de una respuesta correcta por pregunta')
    #print(result)
    return result
    


def fillXML(file):
    result = ""
    wrapper_question = {
        "header": [
            """<?xml version="1.0" encoding="UTF-8"?>
                <quiz>""",
            """ </quiz>""",
        ],
        "question": [
            """<question type="multichoice">
                    <name>
                        <text>""",
                    """</text>
                    </name>
                    <questiontext format="html">
                        <text>""",
                    """</text>
                    </questiontext>
                        <defaultgrade>""",
                    """</defaultgrade>
                    <penalty>""",
                """</penalty>
                    <hidden>0</hidden>
                    <single>true</single>
                    <shuffleanswers>true</shuffleanswers>
                    <answernumbering>abc</answernumbering>
                    """,
                """
                    </question>
                """
        ],
        "correct_answ": [
            """
                <answer fraction="100">
                    <text>""",
                """</text>
                </answer>
            """,
        ],
        "wrong_answ": [
            """
                <answer fraction=""",
                """><text>""",
                """</text>
                </answer>
            """,
        ],
    }
    #empezamos a rellenar el archivo MoodleXML
    result += wrapper_question["header"][0]
    for q in file:
        mistake_fraction = 100 / (len(q["question"]) - 1)
        question_xml = ""
        try:
            #nombre, texto, penalización por intentos y puntuación por defecto
            question_xml += wrapper_question["question"][0] # inicio pregunta
            question_xml += q["question"][0]
            question_xml += wrapper_question["question"][1]  # texto pregunta
            question_xml += q["question"][0]
            question_xml += wrapper_question["question"][2] # puntos por defecto
            question_xml += str(q["puntuation"])
            question_xml += wrapper_question["question"][3] # penalización por repetición
            question_xml += str(q["penalization"])
            question_xml += wrapper_question["question"][4] # final de opción incorrecta

            #opciones
            #opción correcta
            answers = parseCorrectWrong(q['question'])
            question_xml += wrapper_question['correct_answ'][0] # inicio de opción correcta
            question_xml += answers['correct'][0]
            question_xml += wrapper_question['correct_answ'][1] # final de opción correcta
            
            #opciones incorrectas
            for wrong_answer in answers["wrong"]:
                penalization = q['penalization']
                question_xml += wrapper_question["wrong_answ"][0] # inicio de opción incorrecta
                question_xml += f'\"-{mistake_fraction}\"'
                question_xml += wrapper_question["wrong_answ"][1] # inicio de texto opción incorrecta
                question_xml += wrong_answer
                question_xml += wrapper_question["wrong_answ"][2] # final de opción incorrecta
            result += question_xml
            result += wrapper_question['question'][5]
        except Exception as e:
            print(f'Ha habido una excepción:{type(e).__name__}--{e}')
    result += wrapper_question["header"][1]
    return result

def fillAiken(file):
    pass


def convert(file_name, save_file_name, file_type='moodleXML'):
    file = readFile(file_name)
    output_file_content = ''
    match (file_type):
        case "moodleXML":
            output_file_content = fillXML(file)
        case "aiken":
            output_file_content = fillAiken(file)
        case _:
            output_file_content = fillXML(file)
    print(output_file_content)
    writeFile(output_file_content, save_file_name)
    print('Archivo escrito')
