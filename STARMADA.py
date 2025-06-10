from re import sub
print('함대를 업로드하세요 (ctrl V 후 Enter)\n경고창은 무시해도 됩니다\n')
Fleet = []
while True:
    line = input()
    if line.strip() == '':  # Skip blank lines
        continue

    # 아디 갈리아 오타 문제
    line = line.replace('GAllia', 'Gallia')

    # 베이더 중복 문제
    line = line.replace('Darth Vader (1)', 'Darth Vader (officer) (1)')
    line = line.replace('Darth Vader (4)', 'Darth Vader (officer) (4)')
    line = line.replace('Darth Vader (3)', 'Darth Vader (boarding) (3)')
    line = line.replace('다스 베이더 (4)', '다스 베이더 (officer) (4)')
    line = line.replace('다스 베이더 (3)', '다스 베이더 (boarding) (3)')


    # 아소카 중복 문제
    line = line.replace('Ahsoka Tano (2)', 'Ahsoka Tano (Rebel) (2)')
    line = line.replace('Ahsoka Tano (6)', 'Ahsoka Tano (Republic) (6)')
    line = line.replace('아소카 타노 (2)', 'Ahsoka Tano (Rebel) (2)')
    line = line.replace('아소카 타노 (6)', 'Ahsoka Tano (Republic) (6)')
    
    line = sub(r'\((\d+)\)','',line.strip())

    Fleet.append(line)
    if 'Total Points:' in line:
        break


FleetInfo = {} 

for item_string in Fleet:
    if item_string == 'Squadrons:' : break
    parts = item_string.split(':', 1)

    if len(parts) == 2:

        key = parts[0].strip()
        value = parts[1].strip()
        FleetInfo[key] = value
    else:
       break
Name = FleetInfo.get('Name')
Faction = FleetInfo.get('Faction').replace('Empire', 'Imperial')
Commander = FleetInfo.get('Commander','')
Fleetlist = [[Faction, FleetInfo.get('Assault',''), FleetInfo.get('Defense',''), FleetInfo.get('Navigation','')]]

Fleet = Fleet[len(FleetInfo):]

ship = True

for i in range(len(Fleet)) :
    card = Fleet[i]
    if card.strip() == 'Squadrons:' : # 스쿼드론
        ShipCount = len(Fleetlist) - 1
        Fleetlist.append([])
        ship = False
        continue
    elif card[:13] == 'Total Points:' :
        break
    elif card[0] == '=' : # 함선 끝
        continue
    elif card[0] != '•' : # 함선
        Fleetlist.append([card.strip()])
    else: # 업그레이드
        if ship : # 업그레이드
            Fleetlist[-1].append(card[2:].strip())
        else: #스쿼드론
            squadron = sub(r'^\d+\s*x\s*','',card[2:])
            # Star-Forge
            if Faction == 'Rebel' :
                squadron = squadron.replace('Hera Syndulla - Ghost', 'Hera Syndulla (Ghost)')
                squadron = squadron.replace('Hera Syndulla - X-wing Squadron', 'Hera Syndulla (X-wing)')
            elif Faction == 'Imperial' :
                squadron = squadron.replace('Darth Vader - TIE Advanced Squadron', 'Darth Vader (TIE Advanced)')
                squadron = squadron.replace('Darth Vader - TIE Defender Squadron', 'Darth Vader (TIE Defender)')
            elif Faction == 'Republic' :
                squadron = squadron.replace('Anakin Skywalker - BTL-B Y-wing Squadron', 'Anakin Skywalker (BTL-B)')
                squadron = squadron.replace('Anakin Skywalker - Delta-7 Aethersprite Squadron', 'Anakin Skywalker (Delta-7)')
                squadron = squadron.replace('Anakin Skywalker - Twilight', 'Anakin Skywalker (Twilight)')
            else : pass
            squadron = squadron.split(' - ')[0]
            Fleetlist[-1].append(squadron.strip())


# 여기까지, 함대 리스트 만들기

# 함장은 다른 업그레이드와 구분해야 함
# 함선은 진영별로 구분해야 함

for i in range(1, len(Fleetlist)) :
    for j in range(len(Fleetlist[i])) :
        if str(Fleetlist[i][j]) == str(Commander) :
            Fleetlist[i][j] = Fleetlist[i][j] + ' (commander)'

for i in range(1, 4) :
    if str(Fleetlist[0][i]) == '' :
        Fleetlist[0][i] = 'Blank'

for i in range(1, len(Fleetlist) - 1) :
    Fleetlist[i][0] = Fleetlist[i][0] + ' (' + str(Faction) + ')'

print()
print(Fleetlist)






# 파일 위치 찾기
from os import path, makedirs
address = path.realpath(__file__)
address = address[:address.rfind('\\')]
address = address[:address.rfind('\\')] # exe에서는 internal 폴더가 만들어지기 때문
address = address.replace('\\','/')

main_link_filename = f'{address}/resources/Card Link.csv'
upgrade_link_filename = f'{address}/resources/Upgrade Link.csv'


from csv import reader  
def read_csv_to_dict(filename):
    # Read the CSV file content
    with open(filename, 'r', encoding='utf-8') as file:
        readdata = reader(file)
        data = []
        for row in readdata:
            # Skip blank rows
            if any(cell.strip() for cell in row):
                data.append(row)

    # Get the header row
    header = [h.strip() for h in data[0]] # Strip whitespace from header elements

    # Find the indices of 'Eng' and 'Kor' columns

    eng_col_index = header.index('Eng')
    kor_col_index = header.index('Kor')


    # Create a dictionary to store the mapping
    eng_kor_map = {}
    for row in data[1:]:  # Skip the header row
        if row[eng_col_index].strip():  # Ensure the Eng column is not blank
            eng_kor_map[row[eng_col_index].strip()] = row[kor_col_index].strip()
    return eng_kor_map

mainmap = read_csv_to_dict(main_link_filename)
upgrademap = read_csv_to_dict(upgrade_link_filename)


# Function to find the Kor value for a given Eng string
def maindata(eng_string):
    return mainmap.get(eng_string.strip())
def upgradedata(eng_string):
    return upgrademap.get(eng_string.strip())



from PIL import Image

ImageList = list(range(len(Fleetlist)))
for i in range(len(Fleetlist)) :
    ImageList[i] = []




try : # 엑셀 링크 오류 시 경고문 프린트
    for i in range(len(Fleetlist[0])) :
        currentIMG = str(Fleetlist[0][i])
        link = maindata(str(Fleetlist[0][i]))
        link = address + str(link)
        print(link)
        ImageList[0].append(Image.open(link))

    for i in range(1, len(Fleetlist) - 1) :
        currentIMG = str(Fleetlist[i][0])
        link = maindata(str(Fleetlist[i][0]))
        link = address + str(link)
        print(link)
        ImageList[i].append(Image.open(link))

        for j in range(1, len(Fleetlist[i])) :
            currentIMG = str(Fleetlist[i][j])
            link = upgradedata(str(Fleetlist[i][j]))
            link = address + str(link)
            print(link)
            ImageList[i].append(Image.open(link))

    for i in range(len(Fleetlist[len(Fleetlist) - 1])) :
        currentIMG = str(Fleetlist[len(Fleetlist) - 1][i])
        link = maindata(str(Fleetlist[len(Fleetlist) - 1][i]))
        link = address + str(link)
        print(link)
        ImageList[len(ImageList) - 1].append(Image.open(link))
except :
    print(f'"{currentIMG}" 카드를 찾을 수 없습니다. "{currentIMG}"에 오타가 있거나, resources 폴더의 STARMADA Link csv 파일에서 "{currentIMG}" 카드의 영문 또는 한글 이름 및 경로를 확인해 수정해주세요!')
    from time import sleep
    sleep(10)
    exit()

# 여기까지, 이미지 리스트 만들기


def flatten_image(image, background_color=(255, 255, 255)):
    '''Flattens an RGBA image onto a solid background.'''
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    bg = Image.new('RGBA', image.size, background_color + (255,))
    bg.paste(image, (0, 0), image)
    return bg



from shutil import rmtree
from datetime import datetime

FileName = f'{address}/Fleetlist/' + Name + ' (' + datetime.today().strftime('%Y%m%d') + ') (' + Faction + ')'
makedirs(FileName, exist_ok=True)
rmtree(FileName)
makedirs(FileName)

output = []

FleetImage = list(range(len(Fleetlist)))

FleetImage[0] = Image.new('RGBA', (3508, 2480), (255, 255, 255,0))
for i in range(3) :
    FleetImage[0].paste(ImageList[0][i + 1], (100 + 800 * i, 100))
FleetImage[0].paste(ImageList[0][0], (3100, 100))

flatten_image(FleetImage[0]).save(FileName + '/Objectives.webp', format='WEBP', quality=100)
output.append(flatten_image(FleetImage[0]).convert('RGB'))

print('Processing...')

from math import ceil

for ShipNumber in range(ShipCount) :
    ShipNumber += 1
    if Fleetlist[ShipNumber][0].find('SSD') == -1 and Fleetlist[ShipNumber][0].find('Star Dreadnought') == -1 :

        UpgradeCount = len(Fleetlist[ShipNumber]) - 1
        if UpgradeCount <= 6 :
            FleetImage[ShipNumber] = Image.new('RGBA', (3508, 2480), (255, 255, 255,0))
            FleetImage[ShipNumber].paste(ImageList[ShipNumber][0], (100, 100))
            for UpgradeNumber in range(UpgradeCount) :
                x = 1000 + 800 * (UpgradeNumber % 3)
                y = 100 + 1100 * (UpgradeNumber // 3)
                FleetImage[ShipNumber].paste(ImageList[ShipNumber][UpgradeNumber + 1], (x, y))
            flatten_image(FleetImage[ShipNumber]).save(FileName + '/Ship' + str(ShipNumber) + '.webp', format='WEBP', quality=100)
            output.append(flatten_image(FleetImage[ShipNumber]).convert('RGB'))

        else :
            FleetImage[ShipNumber] = Image.new('RGBA', (7016, 2480), (255, 255, 255,0))
            FleetImage[ShipNumber].paste(ImageList[ShipNumber][0], (100, 100))
            for UpgradeNumber in range(UpgradeCount) :
                x = 1000 + 800 * (UpgradeNumber % ((UpgradeCount + 1) // 2))
                y = 100 + 1100 * (UpgradeNumber // ((UpgradeCount + 1) // 2))
                FleetImage[ShipNumber].paste(ImageList[ShipNumber][UpgradeNumber + 1], (x, y))
            
            Ship1 = FleetImage[ShipNumber]
            Ship2 = FleetImage[ShipNumber]

            Ship1Cropped = Ship1.crop((0, 0, 3400, 2480))
            Ship2Cropped = Ship2.crop((3400, 0, 6600, 2480))
            
            Ship1Resized = Image.new('RGBA', (3508, 2480), (255, 255, 255,0))
            Ship2Resized = Image.new('RGBA', (3508, 2480), (255, 255, 255,0))
            Ship1Resized.paste(Ship1Cropped, (0, 0))
            Ship2Resized.paste(Ship2Cropped, (100, 0))

            flatten_image(Ship1Resized).save(FileName + '/Ship' + str(ShipNumber) + '(1).webp', format='WEBP', quality=100)
            flatten_image(Ship2Resized).save(FileName + '/Ship' + str(ShipNumber) + '(2).webp', format='WEBP', quality=100)
            output.append(flatten_image(Ship1Resized).convert('RGB'))
            output.append(flatten_image(Ship2Resized).convert('RGB'))
        print('Ship' + str(ShipNumber) + ' saved')

    else :
        
        UpgradeCount = len(Fleetlist[ShipNumber]) - 1
        
        if UpgradeCount <= 4 :
            FleetImage[ShipNumber] = Image.new('RGBA', (3508, 2480), (255, 255, 255,0))
            FleetImage[ShipNumber].paste(ImageList[ShipNumber][0], (100, 100))
            for UpgradeNumber in range(UpgradeCount) :
                x = 1673 + 800 * (UpgradeNumber % 2)
                y = 100 + 1100 * (UpgradeNumber // 2)
                FleetImage[ShipNumber].paste(ImageList[ShipNumber][UpgradeNumber + 1], (x, y))
            flatten_image(FleetImage[ShipNumber]).save(FileName + '/Ship' + str(ShipNumber) + '.webp', format='WEBP', quality=100)
            output.append(flatten_image(FleetImage[ShipNumber]).convert('RGB'))

        elif 4 < UpgradeCount <= 12 :
            FleetImage[ShipNumber] = Image.new('RGBA', (7016, 2480), (255, 255, 255,0))
            FleetImage[ShipNumber].paste(ImageList[ShipNumber][0], (100, 100))
            for UpgradeNumber in range(UpgradeCount) :
                x = 1673 + 800 * (UpgradeNumber % ceil(UpgradeCount / 2))
                y = 100 + 1100 * (UpgradeNumber // ceil(UpgradeCount / 2))
                FleetImage[ShipNumber].paste(ImageList[ShipNumber][UpgradeNumber + 1], (x, y))
            
            Ship1 = FleetImage[ShipNumber]
            Ship2 = FleetImage[ShipNumber]

            Ship1Cropped = Ship1.crop((0, 0, 3273, 2480))
            Ship2Cropped = Ship2.crop((3273, 0, 6473, 2480))

            Ship1Resized = Image.new('RGBA', (3508, 2480), (255, 255, 255,0))
            Ship2Resized = Image.new('RGBA', (3508, 2480), (255, 255, 255,0))
            Ship1Resized.paste(Ship1Cropped, (0, 0))
            Ship2Resized.paste(Ship2Cropped, (100, 0))

            flatten_image(Ship1Resized).save(FileName + '/Ship' + str(ShipNumber) + '(1).webp', format='WEBP', quality=100)
            flatten_image(Ship2Resized).save(FileName + '/Ship' + str(ShipNumber) + '(2).webp', format='WEBP', quality=100)
            output.append(flatten_image(Ship1Resized).convert('RGB'))
            output.append(flatten_image(Ship2Resized).convert('RGB'))



        else : 
            FleetImage[ShipNumber] = Image.new('RGBA', (10524, 2480), (255, 255, 255,0))
            FleetImage[ShipNumber].paste(ImageList[ShipNumber][0], (100, 100))
            for UpgradeNumber in range(UpgradeCount) :
                x = 1673 + 800 * (UpgradeNumber % ceil(UpgradeCount / 2))
                y = 100 + 1100 * (UpgradeNumber // ceil(UpgradeCount / 2))
                FleetImage[ShipNumber].paste(ImageList[ShipNumber][UpgradeNumber + 1], (x, y))
            
            Ship1 = FleetImage[ShipNumber]
            Ship2 = FleetImage[ShipNumber]
            Ship3 = FleetImage[ShipNumber]

            Ship1Cropped = Ship1.crop((0, 0, 3273, 2480))
            Ship2Cropped = Ship2.crop((3273, 0, 6473, 2480))
            Ship3Cropped = Ship3.crop((6473, 0, 9673, 2480))

            Ship1Resized = Image.new('RGBA', (3508, 2480), (255, 255, 255, 0))
            Ship2Resized = Image.new('RGBA', (3508, 2480), (255, 255, 255, 0))
            Ship3Resized = Image.new('RGBA', (3508, 2480), (255, 255, 255, 0))
            Ship1Resized.paste(Ship1Cropped, (0, 0))
            Ship2Resized.paste(Ship2Cropped, (100, 0))
            Ship3Resized.paste(Ship3Cropped, (100, 0))

            flatten_image(Ship1Resized).save(FileName + '/Ship' + str(ShipNumber) + '(1).webp', format='WEBP', quality=100)
            flatten_image(Ship2Resized).save(FileName + '/Ship' + str(ShipNumber) + '(2).webp', format='WEBP', quality=100)
            flatten_image(Ship3Resized).save(FileName + '/Ship' + str(ShipNumber) + '(3).webp', format='WEBP', quality=100)
            output.append(flatten_image(Ship1Resized).convert('RGB'))
            output.append(flatten_image(Ship2Resized).convert('RGB'))
            output.append(flatten_image(Ship3Resized).convert('RGB'))

        print('Ship' + str(ShipNumber) + ' saved')
    
SquadronCount = len(Fleetlist[ShipCount + 1])
if SquadronCount > 0 :    
    SquadronPageCount = SquadronCount // 8 + 1
    FleetImage[ShipCount + 1] = list(range(SquadronPageCount))
    for i in FleetImage[ShipCount + 1] :
        FleetImage[ShipCount + 1][i] = Image.new('RGBA', (3508, 2480), (255, 255, 255, 0))

    for SquadronNumber in range(SquadronCount) : 
        FleetImage[ShipCount + 1][SquadronNumber // 8].paste(ImageList[ShipCount + 1][SquadronNumber], (100 + 800 * (SquadronNumber % 4), 100 + 1100 * ((SquadronNumber % 8) // 4)))

    for SquadronPage in range(SquadronPageCount) :
        flatten_image(FleetImage[ShipCount + 1][SquadronPage]).save(FileName + '/Squadron' + str(SquadronPage + 1) + '.webp', format='WEBP', quality=100)
        output.append(flatten_image(FleetImage[ShipCount + 1][SquadronPage]).convert('RGB'))
    print('Squadron saved')

output[0].save(FileName + '/@' + Name + '.pdf',quality=100, save_all=True, append_images=output[1:])
from os import startfile
startfile(FileName)


# 파이썬에서 실행시 'address = address[:address.rfind('\\')] # exe에서는 internal 폴더가 만들어지기 때문' 주석처리하고 실행
# exe 변환할 때는 다시 주석해제
# pyinstaller -i 'C:\STARMADA\ico\STARMADA.ico' 'C:\STARMADA\STARMADA_dist\STARMADA.py'  --noconfirm --clean --upx-dir='C:\Users\tanti\Desktop\upx-5.0.1-win64'
