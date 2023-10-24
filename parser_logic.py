from icecream import ic

def read_file(file_name):
    cleaned_lines = []
    result = []
    with open(
        "E:\proyectosPersonales\scriptsPython\parserCuestionarioXML\preguntas_sample.txt",
        "r",
        encoding="UTF8",
    ) as file:
        lines = file.read().split("\n\n")
        cleaned_lines = [q for q in lines if q != ""]  # filtro de vacías
        # print(cleaned_lines)
        for q in cleaned_lines:
            q_lines = q.split("\n")
            first_line = q_lines[0].split("|")
            # print(first_line)
            punt = 1
            pen = float(punt) / (
                len(q_lines) - 1
            )  # 1 sola línea en el caso de que no esté especificada la puntuación y penalización
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
    with open(name,'w') as new_file:
        new_file.write(file_content)
def parseCorrectWrong(question):
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
                <answer fraction="0">
                    <text>""",
                """</text>
                </answer>
            """,
        ],
    }
    #empezamos a rellenar el archivo MoodleXML
    result += wrapper_question["header"][0]
    for q in file:
        question_xml = ""
        try:
            #nombre, texto y penalización
            question_xml += wrapper_question["question"][0]
            question_xml += q["question"][0]
            question_xml += wrapper_question["question"][1]
            question_xml += q["question"][0]
            question_xml += wrapper_question["question"][2]
            question_xml += str(q["penalization"])
            question_xml += wrapper_question["question"][3]

            #opciones
            answers = parseCorrectWrong(q['question'])
            question_xml += wrapper_question['correct_answ'][0]
            question_xml += answers['correct'][0]
            question_xml += wrapper_question['correct_answ'][1]
            for wrong_answer in answers["wrong"]:
                question_xml += wrapper_question["wrong_answ"][0]
                question_xml += wrong_answer
                question_xml += wrapper_question["wrong_answ"][1]
            result += question_xml
            result += wrapper_question['question'][4]
        except Exception as e:
            print(f'Ha habido una excepción:{type(e).__name__}--{e}')
    result += wrapper_question["header"][1]
    #print(result)
    return result

def fillAiken(file):
    pass


def __main__():
    file = read_file("hola")
    #print(file)
    file_type = "moodleXML"
    output_file_content = ''
    match (file_type):
        case "moodleXML":
            output_file_content = fillXML(file)
        case "aiken":
            fillAiken(file)
        case _:
            fillXML(file)
    print(output_file_content)
    writeFile(output_file_content, './pruebaXML.xml')
if __name__ == "__main__":
    __main__()