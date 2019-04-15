# All characters mentioned in PyRy's code except Z and z, reserved for the membranes
CHAIN_NAMES = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","W","X","Y",\
                       "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","w","x","y",\
                       "1","2","3","4","5","6","7","8","9","0","-","+","_","=","~","`","!","@","#","$","%","^","&","*","(",\
                       ")","{","}","[","]","|"]

DIMER_COUNT = 2

RESFILENAME = "cadherins_restraints_" + str(DIMER_COUNT) + ".txt"

RFN = open(RESFILENAME, "w")

for i in range(0, DIMER_COUNT):
    mono1 = CHAIN_NAMES[:5]
    del(CHAIN_NAMES[:5])
    mono2 = CHAIN_NAMES[:5]
    del(CHAIN_NAMES[:5])

    # interaction between "first" domains of two monomers
    print >> RFN, "dist((1-101) \"" + mono1[0] + "\"-(1-101) \"" + mono2[0] + "\" (<=5))"

    # interaction between "last" domains and their assigned membranes
    print >> RFN, "dist((99-108) \"" + mono1[-1] + "\"-(1-400) \"z\" (<=5))"
    print >> RFN, "dist((99-108) \"" + mono2[-1] + "\"-(1-400) \"Z\" (<=5))"

    # covalent bonds between domains - monomer 1
    print >> RFN, "dist((101) \"" + mono1[0] + "\"-(1) \"" + mono1[1] + "\" (<=3.5))"
    print >> RFN, "dist((113) \"" + mono1[1] + "\"-(1) \"" + mono1[2] + "\" (<=3.5))"
    print >> RFN, "dist((117) \"" + mono1[2] + "\"-(1) \"" + mono1[3] + "\" (<=3.5))"
    print >> RFN, "dist((105) \"" + mono1[3] + "\"-(1) \"" + mono1[4] + "\" (<=3.5))"

    # covalent bonds between domains - monomer 2
    print >> RFN, "dist((101) \"" + mono2[0] + "\"-(1) \"" + mono2[1] + "\" (<=3.5))"
    print >> RFN, "dist((113) \"" + mono2[1] + "\"-(1) \"" + mono2[2] + "\" (<=3.5))"
    print >> RFN, "dist((117) \"" + mono2[2] + "\"-(1) \"" + mono2[3] + "\" (<=3.5))"
    print >> RFN, "dist((105) \"" + mono2[3] + "\"-(1) \"" + mono2[4] + "\" (<=3.5))"
    
