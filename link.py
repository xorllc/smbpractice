import sys

def patch_chr(c):
	c = bytearray(c)

	title = [
		0x20, 0xAB, 0x0B, 0x10, 0x12, 0x1D, 0x11, 0x1E, 0x0B, 0xAF, 0x0C, 0x18, 0x16, 0x21, 0x20, 0xCB, 0x09, 0x19, 0x0E, 0x15, 0x15, 0x1C, 0x1C, 0x18, 0x17, 0x21, 0x20, 0xEB, 0x0B, 0x1C, 0x16, 0x0B, 0x19, 0x1B, 0x0A, 0x0C, 0x1D, 0x12, 0x0C, 0x0E, 0x21, 0x05, 0x01, 0x44, 0x21, 0x06, 0x54, 0x48, 0x21, 0x1A, 0x01, 0x49, 0x21, 0x25, 0xC5, 0x46, 0x21, 0x26, 0x15, 0xD0, 0xE8, 0xD1, 0xD0, 0xD1, 0xDE, 0xD1, 0xD8, 0xD0, 0xD1, 0x26, 0xDE, 0xD1, 0xDE, 0xD1, 0xD0, 0xD1, 0xD0, 0xD1, 0x26, 0x4A, 0x21, 0x46, 0xC4, 0xDB, 0x21, 0x47, 0x42, 0x42, 0x21, 0x49, 0xC2, 0xDB, 0x21, 0x4A, 0x11, 0x42, 0xDB, 0x42, 0xDB, 0xDB, 0x42, 0x26, 0xDB, 0x42, 0xDB, 0x42, 0xDB, 0x42, 0xDB, 0x42, 0x26, 0x4A, 0x21, 0x67, 0x45, 0xDB, 0x21, 0x6C, 0x0F, 0xDF, 0xDB, 0xDB, 0xDB, 0x26, 0xDB, 0xDF, 0xDB, 0xDF, 0xDB, 0xDB, 0xE4, 0xE5, 0x26, 0x4A, 0x21, 0x87, 0x42, 0xDB, 0x21, 0x89, 0x12, 0xDE, 0x43, 0xDB, 0xE0, 0xDB, 0xDB, 0xDB, 0x26, 0xDB, 0xE3, 0xDB, 0xE0, 0xDB, 0xDB, 0xE6, 0xE3, 0x26, 0x4A, 0x21, 0xA7, 0x43, 0xDB, 0x21, 0xAA, 0x11, 0x42, 0xDB, 0xDB, 0xDB, 0xD4, 0xD9, 0x26, 0xDB, 0xD9, 0xDB, 0xDB, 0xD4, 0xD9, 0xD4, 0xD9, 0xE7, 0x4A, 0x21, 0xC5, 0x01, 0x5F, 0x21, 0xC6, 0x48, 0x95, 0x21, 0xCE, 0x0D, 0x97, 0x98, 0x78, 0x95, 0x96, 0x95, 0x95, 0x97, 0x98, 0x97, 0x98, 0x95, 0x7A, 0x21, 0xE5, 0x04, 0x1F, 0x01, 0xAF, 0x00, 0x21, 0xED, 0x0E, 0xCF, 0x01, 0x09, 0x08, 0x05, 0x24, 0x17, 0x12, 0x17, 0x1D, 0x0E, 0x17, 0x0D, 0x18, 0x22, 0x4B, 0x07, 0x01, 0x24, 0x20, 0x18, 0x1B, 0x15, 0x0D, 0x22, 0x8B, 0x07, 0x01, 0x24, 0x15, 0x0E, 0x1F, 0x0E, 0x15, 0x22, 0xEC, 0x04, 0x1B, 0x1E, 0x15, 0x0E, 0x23, 0xC9, 0x56, 0x55, 0x23, 0xE2, 0x04, 0x99, 0xAA, 0xAA, 0xAA, 0x23, 0xEA, 0x04, 0x99, 0xAA, 0xAA, 0xAA, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF
	]

	slash = [ 0x06, 0x0e, 0x1c, 0x38, 0x70, 0xe0, 0xc0 ]

	# patch X for /
	for i in range(0, len(slash)):
		c[0x1210 + i] = slash[i]
	return c[0:0x1ec0] + bytearray(title)

print('Building INES image from output...')

prg = open('smb.bin', 'rb').read()

if len(prg) > 0x8000:
	print('Too big prg rom by %d bytes' % (len(prg) - 0x8000))
	sys.exit(-1)

ines = open('ines.bin', 'rb').read()
gfx = patch_chr(open('smb-org.nes', 'rb').read()[len(ines)+0x8000:])

interrupts = prg[-6:]
prg = prg[:-6]
pad = bytearray([ 0xEA ] * (0x8000 - (len(prg) + len(interrupts))))

print('Adding %d bytes of padding before interrupts...' % (len(pad)))

open('smb-hack.chr', 'wb').write(gfx)
open('smb-hack.nes', 'wb').write(ines + prg + pad + interrupts + gfx)



