from Buffer import Buffer
import ndspy.rom
from nlzss import lzss3
from Formats import Item
import random


def run():
    rom = ndspy.rom.NintendoDSRom.fromFile('FE12.nds')
    # for idx in range(len(rom.files)):
    #     print(rom.filenames.filenameOf(idx))
    data = rom.getFileByName('data/FE12Data.bin')
    data = modify(lzss3.decompress_bytes(data))
    data = lzss3.compress(data)
    rom.setFileByName('data/FE12Data.bin', data)

    with open('FE12_new.nds', 'wb') as f:
        f.write(rom.save())
    print('ROM write success')


def modify(data):
    random.seed()
    buffer = Buffer(data)
    buffer.seek_global(0xa308)
    items = []
    for idx in range(193):
        items.append(Item(buffer, idx))

    max_hit = 0
    max_uses = 0
    max_might = 0
    max_crit = 0
    for idx in range(0xA8):
        weapon = items[idx]
        if weapon.hit > max_hit:
            max_hit = weapon.hit
        if weapon.uses > max_uses:
            max_uses = weapon.uses
        if weapon.might > max_might:
            max_might = weapon.might
        if weapon.crit > max_crit:
            max_crit = weapon.crit

    print('Max hit: %i' % max_hit)
    print('Max uses: %i' % max_uses)
    print('Max might: %i' % max_might)
    print('Max crit: %i' % max_crit)

    for idx in range(0xA8):
        if idx < 0x47 or (idx > 0x85 and idx < 0xA8):
           if idx != 0x36 and idx != 0x37 and idx != 0x38 and idx != 0x3B and idx != 0x3D and idx != 0x3E and idx != 0x3F and idx != 0x40 and idx != 0x41:
                weapon = items[idx]
                if idx != 0x0f:
                    weapon.uses = random.randint(1, 40)
                weapon.might = random.randint(0, 13)
                weapon.hit = random.randint(30, 100)
                weapon.crit = random.randint(0, 20)
                weapon.effectiveness = assign_weakness(weapon.item_type, weapon.effectiveness)
                weapon.ability_1 = assign_ability_1()
                items[idx] = weapon

    #compile time
    buffer.seek_global(0xa308)
    buffer.toggle_write(True)
    for item in items:
        buffer.write_bytes(item.write())

    return buffer.data


if __name__ == '__main__':
    run()

def assign_weakness(type, initial_effective):
    weak_range = random.randint(0, 99)

    if weak_range <= 3:
        effects = [1, 4, 128, 20, 3, 16, 32, 8]
        #effects = [wyrmslayer, armorslayer, swordslayer, rapier, falchion, ridersbane, wingslayer, thunderbolt]
        return random.choice(effects)
    elif type == 3 and weak_range > 3:
        return 32
    else:
        return initial_effective

def assign_ability_1(initial_ability):
    abilities = [64, 4, 2]
    #abilities = [devil, levin, brave]
    mine = random.randint(0, 99)
    if mine < 3:
        return random.choice(abilities)
    else:
        return initial_ability

def random_might():
    mine = random.randint(0, 13)

def random_crit():
    crit_range = random.randint(0,99)
    if crit_range < 70:
            return random.randint(0, 10)
    else:
        return random.randint(11, 20)
    #generate a random number from 0 to 99
    #if the number is less than 70, generate a crit value between 1 and 10
    #else, generate a crit value between 11 and 20

