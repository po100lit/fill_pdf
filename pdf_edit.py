from fillpdf import fillpdfs
import json
from datetime import datetime
import os


def fill_form(input_data: dict):
    # чтение и печать доступных для заполнения полей
    # read_data = fillpdfs.get_form_fields("input.pdf")
    # pprint(data)

    data = input_data['normal']

    # returns a dictionary of fields
    # Set the returned dictionary values a save to a variable
    # For radio boxes ('Off' = not filled, 'Yes' = filled)

    data_dict = {}

    if data.get('clientName'):  # роль клиента
        client_name = data.get('clientName').split()
        data_dict.update({
            'Check Box 13': 'Yes',
            'Text Field 2': client_name[0],
            'Text Field 3': client_name[1],
            'Text Field 4': client_name[2],
            'Text Field 5': data.get('clientDegree'),
        })
    else:
        data_dict['Check Box 12'] = 'Yes'

    data_dict['fio'] = data['clientFullName']  # ФИО

    if data.get('clientOldFullName'):  # ФИО, если менялось и причина
        old_name = data.get('clientOldFullName').split()
        data_dict.update({
            'Text Field 6': old_name[0],
            'Text Field 7': old_name[1],
            'Text Field 8': old_name[2],
            'Text Field 9': data.get('reasonForChangeFullName'),
        })

    gender = data.get('clientGender')  # галочка пол
    if gender == 'Мужской':
        data_dict['Check Box 36'] = 'Yes'
    else:
        data_dict['Check Box 37'] = 'Yes'

    birthday = datetime.utcfromtimestamp(int(data.get('DOB')) / 1000).strftime('%d %m %y').split()  # дата рождения
    data_dict['Text Field 12'] = ' '.join(birthday[0])
    data_dict['Text Field 13'] = ' '.join(birthday[1])
    data_dict['Text Field 14'] = ' '.join(birthday[2])

    data_dict['Check Box 20'] = 'Off' if data.get('isRuCitizenship') == 'false' else 'Yes'  # галочка гражданство РФ

    data_dict['passport'] = '   '.join(data.get('passportNumber'))  # номер паспорта
    data_dict['pass_series'] = data.get('passportSeries')  # серия паспорта
    data_dict['kp'] = '   '.join(data.get('departmentCode'))  # код подразделения
    issued_by_whom = split_string(data.get('issuedByWhom'), 44)  # кем выдан # доступно 2 строки
    if len(issued_by_whom) == 1:
        data_dict['kv-1'] = issued_by_whom[0]
    else:
        data_dict['kv-1'] = issued_by_whom[0]
        data_dict['kv-2'] = ' '.join(issued_by_whom[1:])
    registration_address = split_string(data.get('registrationAddress'),
                                        88)  # зарегистрирован по адресу # доступно 2 строки
    if len(registration_address) == 1:
        data_dict['zpa-1'] = registration_address[0]
    else:
        data_dict['zpa-1'] = registration_address[0]
        data_dict['zpa-2'] = ' '.join(registration_address[1:])
    pass_doi = datetime.utcfromtimestamp(int(data.get('passportDateOfIssue')) / 1000).strftime(
        '%d %m %y').split()  # дата выдачи паспорта
    data_dict['dv-d'] = ' '.join(pass_doi[0])
    data_dict['dv-m'] = ' '.join(pass_doi[1])
    data_dict['dv-y'] = ' '.join(pass_doi[2])

    snils = '   '.join(data.get('clientSnils'))
    data_dict['snils'] = snils[:19] + snils[20:]  # СНИЛС
    data_dict['Text Field 51'] = '   '.join(data.get('clientINN'))  # ИНН
    data_dict['Text Field 43'] = data.get('clientEmail')  # e-mail
    data_dict['Text Field 44'] = data.get('clientPhoneNumber')  # mobile
    data_dict['Text Field 45'] = data.get('clientHomePhoneNumber')  # home phone
    data_dict['Text Field 46'] = data.get('relativeNameAndPhoneNumber')  # имя и телефон родственника
    data_dict['Text Field 47'] = data.get('clientDriverLicense')  # водительское
    data_dict['Text Field 48'] = data.get('clientInternationalPassport')  # загранпаспорт
    data_dict['Text Field 49'] = data.get('clientMilitaryID')  # военный билет

    employment_status = data.get('clientEmploymentStatus')  # статус занятости
    employment_statuses = {
        'Работник/Служащий': 'Check Box 14',
        'Военнослужащий': 'Check Box 15',
        'Не работающий': 'Check Box 16',
        'Работающий пенсионер': 'Check Box 18',
        'Пенсионер': 'Check Box 17',
        'Студент': 'Check Box 19',
    }
    data_dict[employment_statuses.get(employment_status)] = 'Yes'

    credit_target_type = data.get('creditTargetType')  # цель кредита
    credit_target_types = {
        'Под залог недвижимости': 'Check Box 23',
        'Нецелевой кредит': 'Check Box 24',
        'Первичный рынок': 'Check Box 21',
        'Вторичный рынок': 'Check Box 22',
    }
    targets = {
        'квартира': 'Check Box 25',
        'апартаменты': 'Check Box 26',
        'таунхаус': 'Check Box 27',
        'дом/участок': 'Check Box 28',
        'ком.помещение': 'Check Box 29',
        'машиноместо': 'Check Box 30',
        'кладовые и прочее': 'Check Box 31',
        'рефинансирование': 'Check Box 25',
    }
    data_dict[credit_target_types.get(credit_target_type)] = 'Yes'
    if credit_target_type in ('Первичный рынок', 'Вторичный рынок'):
        data_dict[targets.get(data.get('creditTraget'))] = 'Yes'

    city_of_acquisition = data.get('cityOfAcquisition')  # регион приобретения
    regions_of_acquisition = {
        'Москва': 'Check Box 33',
        'Санкт-Петербург': 'Check Box 34',
    }
    data_dict[regions_of_acquisition.get(city_of_acquisition)] = 'Yes'
    if city_of_acquisition not in ('Москва', 'Санкт-Петербург'):
        data_dict.update({
            'Text Field 24': city_of_acquisition,  # доступно 2 строки # TODO: решить по переносам без целых слов
            'Check Box 35': 'Yes'
        })

    # data_dict['Text Field 10'] = data.get('objectSeller') # TODO: нет страницы seller на сайте

    data_dict['Text Field 15'] = data.get('appartCost')  # стоимость квартиры
    data_dict['Text Field 16'] = data.get('initialPayment')  # первоначальный взнос
    data_dict['Text Field 17'] = data.get('creditSum')  # сумма кредита
    if data.get('subsidiesAmount'):  # используются субсидии
        data_dict.update({
            'Check Box 38': 'Yes',
            'Text Field 18': data.get('subsidiesAmount'),
        })
    if data.get('matCapitalAmount'):  # используется материнский капитал
        data_dict.update({
            'Check Box 39': 'Yes',
            'Text Field 19': data.get('matCapitalAmount'),
        })
    data_dict['Text Field 20'] = data.get('creditTerm')  # срок кредита
    data_dict['Text Field 21'] = data.get('paymentDate')  # Удобная дата платежа

    payment_type = data.get('paymentType')  # Вид платежа
    payment_types = {
        'Аннуитетный': 'Check Box 40',
        'Дифференцированный': 'Check Box 41',
    }
    data_dict[payment_types.get(payment_type)] = 'Yes'

    income_proof = data.get('incomeProof')  # Подтверждение дохода
    proofs = {
        '2-НДФЛ': 'Check Box 42',
        'Выписка из ПФР': 'Check Box 43',
        'Налоговая декларация': 'Check Box 44',
        'Без подтверждения': 'Check Box 45',
        'Справка о размере пенсии': 'Check Box 46',
        'Справка по форме банка': 'Check Box 47',
        'Выписка из похозяственной книги': 'Check Box 48',
    }
    data_dict[proofs.get(income_proof)] = 'Yes'

    source_initial_payment = data.get('sourceInitialPayment')  # Источник первоначального взноса
    source_initial_payments = {
        'Накопления': 'Check Box 50',
        'Продажа недвижимости': 'Check Box 51',
        'Помощь родственников': 'Check Box 52',
    }
    if source_initial_payment in source_initial_payments:
        data_dict[source_initial_payments.get(source_initial_payment)] = 'Yes'
    else:
        data_dict.update({
            'Check Box 53': 'Yes',
            'Text Field 26': source_initial_payment,
        })

    program_type = data.get('programType')  # Тип программы
    program_types = {
        'Стандартная': 'Check Box 54',
        'По 2-м документам': 'Check Box 55',
        'Семейная ипотека': 'Check Box 56',
        'Военная ипотека': 'Check Box 57',
        'Господдержка 2020': 'gospodderzhka',
    }
    data_dict[program_types.get(program_type)] = 'Yes'

    if data.get('additional1') != 'null':  # Доп. условия Акции
        data_dict['Check Box 58'] = "Yes"
    if data.get('additional2') != 'null':  # Доп. условия Материнский капитал как первоначальный взнос
        data_dict['Check Box 59'] = "Yes"

    # Адрес фактического проживания
    actual_registration_info = data.get('actualRegistrationInfo')
    actual_addresses = {
        'Адрес проживания совпадает с адресом регистрации': 'Check Box 62',
        'Есть только временная регистрация (при отсутствии постоянной)': 'Check Box 63',
    }
    data_dict[actual_addresses.get(actual_registration_info)] = 'Yes'

    data_dict['Text Field 27'] = data.get('actualIndex')  # индекс
    data_dict['Text Field 28'] = data.get('actualCountry')  # страна
    data_dict['Text Field 36'] = data.get('actualRegion')  # Регион проживания (область, край и пр.)
    data_dict['Text Field 35'] = data.get('actualDistrict')  # район
    data_dict['Text Field 37'] = data.get('actualLocality')  # Населенный пункт
    data_dict['Text Field 29'] = data.get('actualStreet')  # Улица
    data_dict['Text Field 30'] = data.get('actualHouse')  # дом
    data_dict['Text Field 31'] = data.get('actualHousing')  # корпус
    data_dict['Text Field 32'] = data.get('actualApartment')  # квартира

    actual_length_of_stay = data.get('actualLengthOfStay').split(',')  # Срок проживания
    data_dict['Text Field 33'] = actual_length_of_stay[0].split()[0]  # лет
    data_dict['Text Field 34'] = actual_length_of_stay[1].split()[0]  # месяцев

    # Основание для проживания
    reason_for_residence = data.get('actualAddressReasonsForResidence')
    reasons_for_residence = {
        'Собственность': 'Check Box 64',
        'Социальный найм': 'Check Box 65',
        'Аренда': 'Check Box 66',
        'Воинская часть': 'Check Box 67',
        'Жилье родственников': 'Check Box 68',
    }
    data_dict[reasons_for_residence.get(reason_for_residence)] = 'Yes'
    if data.get('actualAddressSpecialMarks') == 'Коммунальная квартира':
        data_dict['Check Box 69'] = 'Yes'

    # Образование
    education = data.get('education')
    educations = {
        'Ученая степень': 'Check Box 70',
        'Два высших и более': 'Check Box 71',
        'Высшее': 'Check Box 72',
        'Неоконченное высшее': 'Check Box 73',
        'Среднее специальное': 'Check Box 74',
        'Среднее': 'Check Box 75',
        'Ниже среднего': 'Check Box 76',
        'Российское МВА': 'Check Box 77',
        'Иностранное МВА': 'Check Box 78',
    }
    if education in educations.keys():
        data_dict[educations.get(education)] = 'Yes'
    else:
        data_dict.update({
            'Check Box 79': 'Yes',
            'Text Field 38': education,
        })
    # Семейное положение
    family_status = data.get('familyStatus')
    family_statuses = {
        'Женат/замужем': 'Check Box 80',
        'Гражданский брак': 'Check Box 81',
        'Холост/не замужем': 'Check Box 82',
        'Разведен(-а)': 'Check Box 83',
        'Вдовец/вдова': 'Check Box 84',
    }
    data_dict[family_statuses.get(family_status)] = 'Yes'
    # Брачный контракт
    marriage_contract = data.get('marriageContract')
    contract_types = {
        'Есть': 'Check Box 85',
        'Нет': 'Check Box 86',
        'Будет заключен до сделки': 'Check Box 87',
    }
    data_dict[contract_types.get(marriage_contract)] = 'Yes'
    # Соц.статус супруга(-и)
    partner_social_status = data.get('partnerSocialStatus')
    social_statuses = {
        'Работает': 'Check Box 88',
        'Не работает': 'Check Box 89',
        'На пенсии': 'Check Box 90',
    }
    data_dict[social_statuses.get(partner_social_status)] = 'Yes'

    data_dict['Text Field 39'] = data.get('amountOfChildren')
    data_dict['Text Field 41'] = data.get('childrenAge')
    data_dict['Text Field 40'] = data.get('amountFamily')
    data_dict['Text Field 42'] = data.get('amountDependents')

    if data.get('clientPartTimeJob'):  # работа по совместительству
        data_dict['Check Box 91'] = 'Yes'
    # Тип занятости
    client_employment_type = data.get('clientEmploymentType')
    employment_types = {
        'Коммерческая': 'Check Box 92',
        'Бюджетная': 'Check Box 93',
        'По найму': 'Check Box 97',
        'Пенсионер': 'Check Box 98',
        'ИП': 'Check Box 99',
    }
    if client_employment_type in employment_types.keys():
        data_dict[employment_types.get(client_employment_type)] = 'Yes'
    else:
        data_dict.update({
            'Check Box 94': 'Yes',
            'Text Field 52': data.get('clientBusinessPercentage')
        })

    # Организация
    organization_name = split_string(data.get('organizationName'), 54)  # доступно 2 строки
    if len(organization_name) == 1:
        data_dict['Text Field 58'] = organization_name[0]
    else:
        data_dict['Text Field 58'] = organization_name[0]
        data_dict['Text Field 59'] = organization_name[1]
    organization_actual_address = split_string(data.get('organizationActualAddress'), 54)  # доступно 2 строки
    if len(organization_actual_address) == 1:
        data_dict['Text Field 60'] = organization_actual_address[0]
    else:
        data_dict['Text Field 60'] = organization_actual_address[0]
        data_dict['Text Field 61'] = organization_actual_address[1]
    if data.get('organizationIndustryOther'):
        data_dict.update({
            'Check Box 122': 'Yes',
            'Text Field 76': data.get('organizationIndustryOther'),
        })
    else:
        organization_industry = data.get('organizationIndustry')
        industries = {
            'Адвокат/юрист': 'Check Box 108',
            'Социальная сфера': 'Check Box 109',
            'Транспорт/Судоходство': 'Check Box 110',
            'Сельское хозяйство': 'Check Box 113',
            'Вооруженные силы': 'Check Box 111',
            'Промышленность': 'Check Box 114',
            'Предприятия ТЭК': 'Check Box 112',
            'Строительство': 'Check Box 1010',
            'Органы власти': 'Check Box 1011',
            'Консалтинг': 'Check Box 115',
            'Медицина': 'Check Box 118',
            'Образование': 'Check Box 116',
            'Наука': 'Check Box 119',
            'Туризм': 'Check Box 117',
            'Нотариус': 'Check Box 1012',
            'Торговля': 'Check Box 1013',
            'ИТ/телеком': 'Check Box 120',
            'Финансы': 'Check Box 123',
            'Охрана': 'Check Box 121',
            'Услуги': 'Check Box 124',
        }
        data_dict[industries.get(organization_industry)] = 'Yes'
    # Численность персонала
    organization_staff_amount = data.get('organizationStaffAmount')
    staff_amounts = {
        'менее 10': 'Check Box 100',
        '10–50': 'Check Box 101',
        '50–100': 'Check Box 102',
        '100-200': 'Check Box 103',
        '200-500': 'Check Box 104',
        'более 500': 'Check Box 105',
    }
    data_dict[staff_amounts.get(organization_staff_amount)] = 'Yes'
    data_dict['Text Field 56'] = data.get('organizationWebSite')  # Сайт организации
    data_dict['Text Field 55'] = data.get('organizationPhoneNumber')  # Телефон организации
    data_dict['Text Field 57'] = '   '.join(data.get('organizationINN'))  # ИНН организации

    # Трудовой стаж
    start_of_work_date = datetime.utcfromtimestamp(int(data.get('startOfWorkDate')) / 1000).strftime('%d %m %y').split()
    data_dict['Text Field 62'] = ' '.join(start_of_work_date[0])
    data_dict['Text Field 63'] = ' '.join(start_of_work_date[1])
    data_dict['Text Field 64'] = ' '.join(start_of_work_date[2])
    start_current_work = datetime.utcfromtimestamp(
        int(data.get('startOfWorkInCurrentOrganizationDate')) / 1000).strftime('%d %m %y').split()
    data_dict['Text Field 65'] = ' '.join(start_current_work[0])
    data_dict['Text Field 66'] = ' '.join(start_current_work[1])
    data_dict['Text Field 67'] = ' '.join(start_current_work[2])
    total_work_experience = data.get('totalWorkExperience').split()
    if len(total_work_experience) > 3:
        data_dict['Text Field 68'] = total_work_experience[0]
        data_dict['Text Field 69'] = total_work_experience[2]
    current_work_experience = data.get('currentOrganizationWorkExperience').split()
    if len(current_work_experience) > 3:
        data_dict['Text Field 70'] = current_work_experience[0]
        data_dict['Text Field 71'] = current_work_experience[2]

    lifespan_current_organization = data.get('lifespanCurrentOrganization')  # Существование организации
    lifespans = {
        'До 2 лет': 'Check Box 106106',
        'От 2 до 5 лет': 'Check Box 107107',
        'Более 5 лет': 'Check Box 108108',
    }
    data_dict[lifespans.get(lifespan_current_organization)] = 'Yes'

    job_title = split_string(data.get('jobTitle'), 54)  # Название должности # доступно 2 строки
    if len(job_title) == 1:
        data_dict['Text Field 72'] = job_title[0]
    else:
        data_dict['Text Field 72'] = job_title[0]
        data_dict['Text Field 73'] = ' '.join(job_title[1:])
    data_dict['Text Field 74'] = data.get('nameSalaryBank')  # Название банка
    data_dict['Text Field 75'] = data.get('salaryCardNumber')  # Номер зарплатной/пенсионной карты

    if data.get('isBankEmployee') != 'false':
        data_dict['Check Box 106'] = 'Yes'
    if data.get('isOrganizationBankClient') != 'false':
        data_dict['Check Box 107'] = 'Yes'

    try:
        # Организация (Работа по совместительству)
        if data.get('organizationName2'):
            organization_name_2 = split_string(data.get('organizationName2'), 54)  # доступно 2 строки
            if len(organization_name_2) == 1:
                data_dict['Text Field 115'] = organization_name_2[0]
            else:
                data_dict['Text Field 115'] = organization_name_2[0]
                data_dict['Text Field 118'] = ' '.join(organization_name_2[1:])
            organization_actual_address_2 = split_string(data.get('organizationActualAddress2'),
                                                         54)  # доступно 2 строки
            if len(organization_actual_address_2) == 1:
                data_dict['Text Field 116'] = organization_actual_address_2[0]
            else:
                data_dict['Text Field 116'] = organization_actual_address_2[0]
                data_dict['Text Field 119'] = ' '.join(organization_actual_address_2[1:])
            data_dict['Text Field 125'] = data.get(
                'organizationWebSite2')  # Сайт организации (Работа по совместительству)
            data_dict['Text Field 120'] = data.get(
                'organizationPhoneNumber2')  # Телефон организации (Работа по совместительству)
            data_dict['Text Field 126'] = '   '.join(
                data.get('organizationINN2'))  # ИНН организации (Работа по совместительству)
        if data.get('organizationIndustryOther2'):
            data_dict.update({
                'Check Box 139': 'Yes',
                'Text Field 117': data.get('organizationIndustryOther2'),
            })
        else:
            organization_industry = data.get('organizationIndustry2')
            industries = {
                'Адвокат/юрист': 'Check Box 1032',
                'Социальная сфера': 'Check Box 1035',
                'Транспорт/Судоходство': 'Check Box 131',
                'Сельское хозяйство': 'Check Box 140',
                'Вооруженные силы': 'Check Box 134',
                'Промышленность': 'Check Box 143',
                'Предприятия ТЭК': 'Check Box 137',
                'Строительство': 'Check Box 1033',
                'Органы власти': 'Check Box 1036',
                'Консалтинг': 'Check Box 132',
                'Медицина': 'Check Box 141',
                'Образование': 'Check Box 135',
                'Наука': 'Check Box 144',
                'Туризм': 'Check Box 138',
                'Нотариус': 'Check Box 1034',
                'Торговля': 'Check Box 1037',
                'ИТ/телеком': 'Check Box 133',
                'Финансы': 'Check Box 142',
                'Охрана': 'Check Box 136',
                'Услуги': 'Check Box 145',
            }
            data_dict[industries.get(organization_industry)] = 'Yes'
        # Численность персонала (Работа по совместительству)
        organization_staff_amount = data.get('organizationStaffAmount2')
        staff_amounts = {
            'менее 10': 'Check Box 1038',
            '10–50': 'Check Box 1041',
            '50–100': 'Check Box 1044',
            '100-200': 'Check Box 1040',
            '200-500': 'Check Box 1043',
            'более 500': 'Check Box 1046',
        }
        data_dict[staff_amounts.get(organization_staff_amount)] = 'Yes'

        # Трудовой стаж (Работа по совместительству)
        start_of_work_date = datetime.utcfromtimestamp(int(data.get('startOfWorkDate2')) / 1000).strftime(
            '%d %m %y').split()
        data_dict['Text Field 129'] = ' '.join(start_of_work_date[0])
        data_dict['Text Field 131'] = ' '.join(start_of_work_date[1])
        data_dict['Text Field 133'] = ' '.join(start_of_work_date[2])
        start_current_work = datetime.utcfromtimestamp(
            int(data.get('startOfWorkInCurrentOrganizationDate2')) / 1000).strftime('%d %m %y').split()
        data_dict['Text Field 130'] = ' '.join(start_current_work[0])
        data_dict['Text Field 132'] = ' '.join(start_current_work[1])
        data_dict['Text Field 134'] = ' '.join(start_current_work[2])
        total_work_experience = data.get('totalWorkExperience2').split()
        if len(total_work_experience) > 3:
            data_dict['Text Field 121'] = total_work_experience[0]
            data_dict['Text Field 123'] = total_work_experience[2]
        current_work_experience = data.get('currentOrganizationWorkExperience2').split()
        if len(current_work_experience) > 3:
            data_dict['Text Field 122'] = current_work_experience[0]
            data_dict['Text Field 124'] = current_work_experience[2]

        lifespan_current_organization = data.get(
            'lifespanCurrentOrganization2')  # Существование организации (Работа по совместительству)
        lifespans = {
            'До 2 лет': 'Check Box 1039',
            'От 2 до 5 лет': 'Check Box 1042',
            'Более 5 лет': 'Check Box 1045',
        }
        data_dict[lifespans.get(lifespan_current_organization)] = 'Yes'

        # данные отсутствует в pdf
        # data_dict['Text Field 127'] = data.get('jobTitle2')  # Название должности (Работа по совместительству) # доступно 2 строки
        # data_dict['Text Field 74'] = data.get('nameSalaryBank2')  # Название банка (Работа по совместительству)
        # data_dict['Text Field 75'] = data.get('salaryCardNumber2')  # Номер зарплатной/пенсионной карты (Работа по совместительству)
        #
        # if data.get('isBankEmployee2') != 'false':
        #     data_dict['Check Box 106'] = 'Yes'
        # if data.get('isOrganizationBankClient2') != 'false':
        #     data_dict['Check Box 107'] = 'Yes'
    except Exception as _:
        print(_)

    # Финансы
    amount_basic_income = data.get('amountBasicIncome')  # Основной доход ₽/мес
    if amount_basic_income:
        data_dict.update({
            'Text Field 77': amount_basic_income,
            'Check Box 1015': 'Yes',
        })
    amount_pension = data.get('amountPension')  # Пенсия ₽/мес
    if amount_pension:
        data_dict.update({
            'Text Field 78': amount_pension,
            'Check Box 1014': 'Yes',
        })
    amount_part_time_income = data.get('amountPartTimeIncome')  # Доход по совместительству ₽/мес
    if amount_part_time_income:
        data_dict.update({
            'Text Field 79': amount_part_time_income,
            'Check Box 1017': 'Yes',
        })
    amount_additional_income = data.get('amountAdditionalIncome')  # Иное доходы
    if amount_additional_income:
        data_dict.update({
            'Text Field 80': amount_additional_income,
            'Text Field 83': data.get('sourceAdditionalIncome'),
            'Check Box 1016': 'Yes',
        })
    sum_income = data.get('sumIncome')  # Сумма доходов ₽/мес
    if sum_income:
        data_dict['Text Field 89'] = sum_income
    amount_credit = data.get('amountCredit')  # Кредиты ₽/мес
    if amount_credit:
        data_dict.update({
            'Text Field 84': amount_credit,
            'Check Box 1020': 'Yes',
        })
    amount_aliment = data.get('amountAliment')  # Алименты/судебные решения ₽/мес
    if amount_aliment:
        data_dict.update({
            'Text Field 86': amount_aliment,
            'Check Box 1018': 'Yes',
        })
    amount_additional_expenses = data.get('amountAdditionalExpenses')  # Иное расходы
    if amount_additional_expenses:
        data_dict.update({
            'Text Field 85': amount_additional_expenses,
            'Text Field 88': data.get('sourceAdditionalExpenses'),
            'Check Box 1021': 'Yes',
        })
    sum_expenses = data.get('sumExpenses')  # Сумма расходов ₽/мес
    if sum_expenses:
        data_dict['Text Field 87'] = sum_expenses

    # Транспортное средство
    data_dict['Text Field 90'] = data.get('vehicleBrand1')
    data_dict['Text Field 91'] = data.get('vehiclePrice1')
    data_dict['Text Field 92'] = data.get('vehicleYear1')
    if data.get('vehicleIsDeposit1') != 'false':
        data_dict['Check Box 1019'] = 'Yes'
    data_dict['Text Field 135'] = data.get('vehicleBrand2')
    data_dict['Text Field 136'] = data.get('vehiclePrice2')
    data_dict['Text Field 137'] = data.get('vehicleYear2')
    if data.get('vehicleIsDeposit2') != 'false':
        data_dict['Check Box 1047'] = 'Yes'
    data_dict['Text Field 143'] = data.get('vehicleBrand3')
    data_dict['Text Field 144'] = data.get('vehiclePrice3')
    data_dict['Text Field 145'] = data.get('vehicleYear3')
    if data.get('vehicleIsDeposit3') != 'false':
        data_dict['Check Box 1058'] = 'Yes'

    # Недвижимость
    immovables_type_1 = data.get('immovablesType1')  # Тип объекта 1
    immovables_types_1 = {
        'квартира': 'Check Box 1022',
        'комната': 'Check Box 1023',
        'участок': 'Check Box 1024',
        'дом': 'Check Box 1025',
    }
    data_dict[immovables_types_1.get(immovables_type_1)] = 'Yes'
    immovables_origin_1 = data.get('immovablesOrigin1')  # Тип владения 1
    immovables_origins_1 = {
        'покупка': 'Check Box 1028',
        'дарение': 'Check Box 1029',
        'приватизация': 'Check Box 1030',
        'наследство': 'Check Box 1031',
    }
    data_dict[immovables_origins_1.get(immovables_origin_1)] = 'Yes'
    immovables_is_deposit_1 = data.get('immovablesIsDeposit1')  # В залоге 1
    if immovables_is_deposit_1 == 'false':
        data_dict['Check Box 1027'] = 'Yes'
    else:
        data_dict['Check Box 1026'] = 'Yes'
    data_dict['Text Field 94'] = data.get('immovablesSquare1')
    data_dict['Text Field 95'] = data.get('immovablesShareSize1')
    data_dict['Text Field 96'] = data.get('immovablesPrice1')
    data_dict['Text Field 93'] = data.get('immovablesYear1')
    immovables_address_1 = split_string(data.get('immovablesAddress1'), 54)  # доступно 2 строки
    if len(immovables_address_1) == 1:
        data_dict['Text Field 170'] = immovables_address_1[0]
    else:
        data_dict['Text Field 170'] = immovables_address_1[0]
        data_dict['Text Field 171'] = ' '.join(immovables_address_1[1:])

    try:
        immovables_type_2 = data.get('immovablesType2')  # Тип объекта 2
        immovables_types_2 = {
            'квартира': 'Check Box 1048',
            'комната': 'Check Box 1053',
            'участок': 'Check Box 1049',
            'дом': 'Check Box 1054',
        }
        data_dict[immovables_types_2.get(immovables_type_2)] = 'Yes'
        immovables_origin_2 = data.get('immovablesOrigin2')  # Тип владения 2
        immovables_origins_2 = {
            'покупка': 'Check Box 1051',
            'дарение': 'Check Box 1056',
            'приватизация': 'Check Box 1052',
            'наследство': 'Check Box 1057',
        }
        data_dict[immovables_origins_2.get(immovables_origin_2)] = 'Yes'
        immovables_is_deposit_2 = data.get('immovablesIsDeposit2')  # В залоге 2
        if immovables_is_deposit_2 == 'false':
            data_dict['Check Box 1055'] = 'Yes'
        else:
            data_dict['Check Box 1050'] = 'Yes'
        data_dict['Text Field 139'] = data.get('immovablesSquare2')
        data_dict['Text Field 140'] = data.get('immovablesShareSize2')
        data_dict['Text Field 141'] = data.get('immovablesPrice2')
        data_dict['Text Field 138'] = data.get('immovablesYear2')
        data_dict['Text Field 142'] = data.get('immovablesAddress2')
    except Exception as _:
        print(_)
    try:
        immovables_type_3 = data.get('immovablesType3')  # Тип объекта 3
        immovables_types_3 = {
            'квартира': 'Check Box 1059',
            'комната': 'Check Box 1064',
            'участок': 'Check Box 1060',
            'дом': 'Check Box 1065',
        }
        data_dict[immovables_types_3.get(immovables_type_3)] = 'Yes'
        immovables_origin_3 = data.get('immovablesOrigin3')  # Тип владения 3
        immovables_origins_3 = {
            'покупка': 'Check Box 1062',
            'дарение': 'Check Box 1067',
            'приватизация': 'Check Box 1063',
            'наследство': 'Check Box 1068',
        }
        data_dict[immovables_origins_3.get(immovables_origin_3)] = 'Yes'
        immovables_is_deposit_3 = data.get('immovablesIsDeposit3')  # В залоге 3
        if immovables_is_deposit_3 == 'false':
            data_dict['Check Box 1066'] = 'Yes'
        else:
            data_dict['Check Box 1061'] = 'Yes'
        data_dict['Text Field 147'] = data.get('immovablesSquare3')
        data_dict['Text Field 148'] = data.get('immovablesShareSize3')
        data_dict['Text Field 149'] = data.get('immovablesPrice3')
        data_dict['Text Field 146'] = data.get('immovablesYear3')
        data_dict['Text Field 150'] = data.get('immovablesAddress3')
    except Exception as _:
        print(_)

    # Личное подсобное хозяйство
    try:
        lph_data = data.get('LPHData')  # Данные о ЛПХ
        lph_types = {
            'Веду личное подсобное хозяйство': 'Check Box 154',
            'ЛПХ учтено в похозяйственной книге': 'Check Box 156',
            'Есть земельный участок для веде-': 'Check Box 155',
            'Веду ЛПХ лично': 'Check Box 157',
        }
        data_dict[lph_types.get(lph_data)] = 'Yes'
        if data.get('incomeFromCropProduction'):  # Доход от растениеводства
            data_dict.update({
                'Check Box 1069': 'Yes',
                'Text Field 151': data.get('incomeFromCropProduction'),
            })
        if data.get('incomeFromFarming'):  # от животноводства
            data_dict.update({
                'Check Box 1070': 'Yes',
                'Text Field 152': data.get('incomeFromFarming'),
            })
        if data.get('incomeNonAgr'):  # от несельскохоз. деятельности в сельской местности
            data_dict.update({
                'Check Box 1071': 'Yes',
                'Text Field 153': data.get('incomeNonAgr'),
            })
        if data.get('incomeTotal'):  # Совокупный среднемесячный чистый доход /расход от владения ЛПХ
            data_dict['Text Field 154'] = data.get('incomeTotal')
        lph_date = datetime.utcfromtimestamp(int(data.get('LPHDate')) / 1000).strftime(
            '%d %m %y').split()  # Дата первой записи в похозяйственной книге
        data_dict['Text Field 155'] = ' '.join(lph_date[0])
        data_dict['Text Field 156'] = ' '.join(lph_date[1])
        data_dict['Text Field 157'] = ' '.join(lph_date[2])
    except Exception as _:
        print(_)

    # Прочее
    insurance_conditions = data.get('insuranceConditions')  # Условия страхования
    conditions = {
        'Полный пакет (Выгодный процент по ипотеке)': 'Check Box 125',
        'Обязательный пакет': 'Check Box 129',
    }
    data_dict[conditions.get(insurance_conditions)] = 'Yes'
    executive = data.get('executive')  # Заверения
    executives = {
        'Не являюсь': 'Check Box 126',
        'Являюсь (и обязуюсь заполнить приложение по форме Банка)': 'Check Box 127',
    }
    data_dict[executives.get(executive)] = 'Yes'
    bankrupt = data.get('bankrupt')  # Заверения
    bankrupts = {
        'Не нахожусь': 'Check Box 128',
        'Нахожусь': 'Check Box 130',
    }
    data_dict[bankrupts.get(bankrupt)] = 'Yes'

    # Дополнительная информация
    additional_information = split_string(data.get('additionalInformation'), 110)  # доступно 9 строк
    available_fields = [
        'Text Field 158',
        'Text Field 159',
        'Text Field 160',
        'Text Field 161',
        'Text Field 162',
        'Text Field 164',
        'Text Field 163',
        'Text Field 165',
        'Text Field 166',
    ]
    if len(additional_information) == 1:
        data_dict['Text Field 158'] = additional_information[0]
    else:
        info_length = len(additional_information)
        for index in range(0, info_length):
            data_dict[available_fields[index]] = additional_information[index]

    fillpdfs.write_fillable_pdf('input.pdf', 'out/filled.pdf', data_dict)

    # If you want it flattened:
    # fillpdfs.flatten_pdf('new.pdf', 'newflat.pdf')


def read_json():
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def split_string(input_string: str, max_length: int):
    # Проверка на пустую строку или недопустимую длину
    if not input_string or max_length <= 0:
        return []

    # Разбиваем строку на части не превышающей max_length длины
    split_strings = []
    start = 0
    while start < len(input_string):
        end = start + max_length
        if end >= len(input_string):
            end = len(input_string)
        else:
            # Найдем последний пробел до max_length для разделения слов
            while end > start and input_string[end] != ' ':
                end -= 1

        split_strings.append(input_string[start:end])
        start = end + 1  # Переходим к следующей части

    return split_strings


if __name__ == '__main__':
    if not os.path.isdir('out'):
        os.mkdir('out')
    fill_form(read_json())
