from icecream import ic
from lxml import etree as ET

def addCorrectAnswMXML(question, text):
    correct_answ = ET.SubElement(question, "answer")
    correct_answ.set('fraction','100')
    correct_answ_text = ET.SubElement(correct_answ, "text")
    correct_answ_text.text = text
    return correct_answ

def addPenalizedAnswMXML(question, text, penalization):
    wrong_answ = ET.SubElement(question, "answer")
    wrong_answ.set('fraction', str(-penalization))
    wrong_answ_text = ET.SubElement(wrong_answ, "text")
    wrong_answ_text.text = text
    return wrong_answ

def remove_comments(questions):
    result = []
    for q in questions:
        ic(q)
        if q.strip().startswith("--"):
            print("dentro")
            continue
        else:
            result.append(q)
    return result

def readFile(file_name, penalization_type):
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
        
        ic(extracted_questions)
        print(len(extracted_questions))
        for q in extracted_questions: # limpiar lineas vacías en las preguntas 
            cleaned_questions.append(q.strip())
        cleaned_questions = remove_comments(cleaned_questions)
        for q in cleaned_questions:
            q_lines = q.split("\n")
            first_line = q_lines[0]
            punt = 1
            pen = 50
            answ_options = len(q_lines) - 1 # 1 sola línea en el caso de que no esté especificada la puntuación
            try:
                punt = float(first_line)
                ic(punt)
                answ_options = len(q_lines) - 2 # 2 líneas quitando la puntuación y el enunciado
            except Exception as e:
                print('Usando puntuación 1 para pregunta sin especificar')
            match(penalization_type.lower()):
                case 'repartida':
                    pen = 100 / answ_options
                case _:
                    pen = 50
            result.append(
                {
                    "punctuation": punt,
                    "penalization": pen,
                    "question": q_lines[1:] if answ_options == len(q_lines) - 2 else q_lines,
                }
            )
    return result

def writeFile(file_content, name):
    print(type(file_content))
    with open(name,'wb') as new_file:
        new_file.write(file_content)

def parseCorrectWrong(question):
    #ic(question)
    result = {
        'wrong': [],
        'correct': []
        }
    for answ in question[1:]:
        if answ.startswith('+'):
            result['correct'].append(answ[1:])
        else:
            if answ.startswith('-'):
                result['wrong'].append(answ[1:])
            else:
                result['wrong'].append(answ)
    if len(result['correct']) > 1 or len(result['correct']) == 0:
        raise Exception('No está pensado el programa para tener más de una respuesta correcta por pregunta')
    #print(result)
    return result

def fillXML(file, blank_answer):
    result = ""
    quiz = ET.Element("quiz")
    i = 1
    for q in file:
        try:
            question = ET.SubElement(quiz,"question")
            question.set('type','multichoice')
            question_name = ET.SubElement(question, "name")
            question_name_text = ET.SubElement(question_name, "text")
            question_name_text.text = 'Pregunta ' + str(i)
            question_text = ET.SubElement(question,"questiontext")
            question_text.set('format','html')
            question_text_text = ET.SubElement(question_text,"text")
            question_text_text.text = q['question'][0]
            question_grade = ET.SubElement(question,"defaultgrade")
            question_grade.text = str(q['punctuation'])
            question_pen = ET.SubElement(question, "penalty")
            question_pen.text = '0.333333'
            question_hidden = ET.SubElement(question, "hidden")
            question_hidden.text = '0'
            question_single = ET.SubElement(question, "single")
            question_single.text = 'true'
            question_shuffle = ET.SubElement(question, "shuffleanswers")
            question_shuffle.text = 'true'
            question_numbering = ET.SubElement(question, "answernumbering")
            question_numbering.text = 'abc'

            #opciones
            #opción correcta
            answers = parseCorrectWrong(q['question'])
            addCorrectAnswMXML(question, answers['correct'][0])
            #opciones incorrectas
            for wrong_answer in answers["wrong"]:
                addPenalizedAnswMXML(question, wrong_answer, q['penalization'])
            if blank_answer:
                addPenalizedAnswMXML(question, 'Respuesta en blanco', 0)
            i += 1
        except Exception as e:
            print(f'Ha habido una excepción:{type(e).__name__}--{e}')
    result = ET.tostring(quiz, pretty_print=True, xml_declaration=True, encoding="utf-8")
    return result

def fillAiken(file, blank_answer):
    letters = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
    result = ''
    for q in file:
        i = 0
        result += f'{q['question'][0]}\n' # texto de la pregunta
        answers = parseCorrectWrong(q['question'])
        # opciones incorrectas
        for wrong_answer in answers['wrong']:
            result += f'{letters[i]}. {wrong_answer}\n'
            i += 1
        if blank_answer:
            result += f'{letters[i]}. Respuesta en blanco\n'
            i += 1
        # opcion correcta
        for correct_answer in answers['correct']:
            result += f'{letters[i]}. {correct_answer}\n'
            result += f'ANSWER: {letters[i]}\n\n'
    return result.encode(encoding='utf-8')

def convert(file_name, save_file_name, blank_answer, penalization_type, file_type='moodleXML'):
    file = readFile(file_name, penalization_type)
    output_file_content = ''
    match (file_type.lower()):
        case "moodleXML":
            output_file_content = fillXML(file, blank_answer)
        case "aiken":
            output_file_content = fillAiken(file, blank_answer)
        case _:
            output_file_content = fillXML(file, blank_answer)
    # print(output_file_content)
    writeFile(output_file_content, save_file_name)
    print('Archivo escrito')
