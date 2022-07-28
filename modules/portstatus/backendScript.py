
def backendScript1(input2):

    if input2.swtabledata.sw_name == "Sw1":
        if input2.status == "up":
            input2.status = "down"

        elif input2.status == 'down':
            input2.status = 'up'
        input2.save()

        return input2.swtabledata.sw_name + ' ' + input2.port + ' ' + "durumu değiştirilmiştir"

    return input2.swtabledata.sw_name + ' ' + input2.port + ' ' + "durumu değiştirilMEMİŞTİR"
