from PIL import Image, ImageDraw, ImageFont, ImageEnhance

import sys
import pandas

minus = Image.open("images/minus.png")

s = 2

hom = Image.open("images/hom.png").convert("RGBA")
het = Image.open("images/het.png").convert("RGBA")
nomut = Image.open("images/nomut.png").convert("RGBA")
hetnomut = Image.open("images/hetnomut.png").convert("RGBA")

hom_rs = hom.resize(((int)(hom.size[0] * 0.22 * s),(int)(hom.size[1]* 0.22 * s)))
het_rs = het.resize(((int)(het.size[0] * 0.22 * s),(int)(het.size[1]* 0.22 * s)))
nomut_rs = nomut.resize(((int)(nomut.size[0] * 0.22 * s),(int)(nomut.size[1]* 0.22 * s)))
hetnomut_rs = hetnomut.resize(((int)(hetnomut.size[0] * 0.22 * s),(int)(hetnomut.size[1]* 0.22 * s)))

iconstretch = 0.32 * s
minus = Image.open("images/minus.png").convert("RGBA")
plus = Image.open("images/plus.png").convert("RGBA")

minus_rs = minus.resize(((int)(minus.size[0] * iconstretch),(int)(minus.size[1] * iconstretch)))
plus_rs = plus.resize(((int)(plus.size[0] * iconstretch),(int)(plus.size[1] * iconstretch)))

sal = Image.open("images/sal.png").convert("RGBA")
uc = Image.open("images/UC.png").convert("RGBA")
pi = Image.open("images/PI.png").convert("RGBA")
water = Image.open("images/negativecontrol.png").convert("RGBA")



sal_rs = sal.resize(((int)(sal.size[0] * iconstretch),(int)(sal.size[1] * iconstretch)))
uc_rs = uc.resize(((int)(uc.size[0] * iconstretch),(int)(uc.size[1] * iconstretch)))
pi_rs = pi.resize(((int)(pi.size[0] * iconstretch),(int)(pi.size[1] * iconstretch)))
water_rs = water.resize(((int)(water.size[0] * iconstretch),(int)(water.size[1] * iconstretch)))

default = pi_rs
RECQ4A_ver  = False

global_brightness = 1.0

if(len(sys.argv) < 2):
	print("Usage: Python3 visualizer summary.tsv")
	exit()



data = pandas.read_csv(sys.argv[1], sep = '\t')
data['Sample'] = data['Sample'].astype(str)
#data['NOTES'] = data['NOTES'].astype(str)
print(data)

nsites = data["Site"].nunique()
nsamples = (int) (data.shape[0] / nsites / 2)
sitenames = ["A", "B", "C", 'D', 'E', 'F']
if(RECQ4A_ver):
	sitenames = ["247248", "448449", "450451"]


print("Sites, samples: ", nsites, nsamples)

font_used = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 15 * s)
font_used_big = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 25 * s)
font_used_small = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 8 * s)

image = Image.new("RGBA",((220 + 170 * nsites) * s, (100 + 60 * nsamples) * s),(255,255,255))

draw = ImageDraw.Draw(image)

def drawMinus(x, y):
	image.paste(minus_rs, (x, y))

def displayMutation(x, y, string, fill_col):
	if string == "n/a" or string == "no_reads":
		draw.text((x, y),string, fill = fill_col, font = font_used)
	else:
		number = int(float(string[3:]))
		if(number < 9):
			draw.text((x, y),str(number), fill = fill_col, font = font_used)
		else:
			draw.text((x - 10, y),str(number), fill = fill_col, font = font_used)
		draw.text((x + 15 * s, y),string[0:3], fill = fill_col, font = font_used)

def drawImgWithOpacity(imgname, loc, mask):
	tmp = imgname.copy()
	global global_brightness
	alpha = tmp.split()[3]
	alpha = ImageEnhance.Brightness(alpha).enhance(global_brightness)

	# data=tmp.getdata()  #you'll get a list of tuples
	# newData=[]
	# for a in data:
	# 	cur_opacity = a[3]
	# 	a = a[:3]
	# 	if(global_opacity < 1):
	# 		a = a + (1,)
	# 	else:
	# 		a = a + (cur_opacity,)
	# 	# a = a + (int((cur_opacity * global_opacity)),)
	# 	newData.append(a)
	
	# alpha = alpha.point(lambda i: i * global_opacity)
	#tmp.putdata(newData)

	tmp.putalpha(alpha)
	print("Brightness: ", global_brightness)
	#imgname.putalpha( int(float(global_opacity) * float(255)) )
	image.paste(imgname, (loc[0], loc[1]), tmp)


def displayCard(x, y, mutation1, mutation2, type , nreads = 0, mutation3 = ""):
	stretch2 = 0.22*s;
	iconstretch = 0.32 *s;
	iconshift = -16 * s;
	x -= 50*s;
	global global_brightness

	if(int(nreads) < 50):
		global_brightness = 0.25 +  0.75 * nreads / 50.0

		#print(" !new opacity:", global_brightness)
		print("few reads")
	else:
		global_brightness = 1

	if(type == 0):
		drawImgWithOpacity(nomut_rs, (x, y),nomut_rs)
		#image(nomut, x, y, nomut.width*stretch2, nomut.height*stretch2);
	if(type == 1):
		drawImgWithOpacity(hom_rs, (x, y),hom_rs)
		#image(hom, x, y, hom.width*stretch2, hom.height*stretch2);
	if(type == 2):
		drawImgWithOpacity(hetnomut_rs, (x, y),hetnomut_rs)
		#image(hetnomut, x, y, hetnomut.width*stretch2, hetnomut.height*stretch2);
	if(type == 3 or type == 4):
		drawImgWithOpacity(het_rs, (x, y),het_rs)
		#image(het, x, y, het.width*stretch2, het.height*stretch2);

	#global_opacity = 1.0

	#fill(0, 150);
	#textSize(15*s);
	if(mutation1 == "No mut"):
		mutation1 = "n/a";
	if(mutation2 == "No mut"):
		mutation2 = "n/a";

	fill_c = (0, 0, 0, 150)
	if(nreads < 100):
		fill_c = (255, 0, 0, 150)
	draw.text((x + 100 * s, y + 50 * s), "n = " + str(round(nreads)), fill = fill_c, font = font_used_small)
	fill_c = (0, 0, 0, 150)

	print(mutation1, mutation2)

	

	chimera_shift = 0
	if(type == 4):
		print("displaying chimera")
		chimera_shift = -14

	if(type == 0 or type == 1):
		#only one mutation to display (or no mutation)
		if(mutation1 == "n/a" or mutation1 == "no_reads"):
			fillc = (100, 100, 100, 100 * global_brightness)
		displayMutation((x+20*s),(y+16*2),mutation1, fill_c)
		print(mutation1[1: 3])
		if(mutation1[1: 3] == "el"):
			image.paste(minus_rs, (x + 60*s, y + 32*s + iconshift), minus_rs)
		else:
			if(mutation1[1: 3] == "ns"):
				image.paste(plus_rs, (x + 60*s, y + 32*s + iconshift), plus_rs)

	else:
		#mutation1
		if(mutation1 == "n/a"):
			fillc = (100, 100, 100, 100 * global_brightness)
		displayMutation((x+20*s),(y+8*2) + chimera_shift, mutation1, fill_c)
		if(mutation1[1: 3] == "el"):
			drawImgWithOpacity(minus_rs, (x + 60*s, y + 22*s + iconshift + chimera_shift), minus_rs)
		else:
			if(mutation1[1: 3] == "ns"):
				drawImgWithOpacity(plus_rs, (x + 60*s, y + 22*s + iconshift + chimera_shift), plus_rs)

		#mutation2
		displayMutation((x+20*s), (y+31*2) + chimera_shift * 2, mutation2, fill_c)
		if(mutation2[1: 3] == "el"):
			drawImgWithOpacity(minus_rs, (x + 60*s, y + 45*s + iconshift + chimera_shift * 2), minus_rs)
		else:
			if(mutation2[1: 3] == "ns"):
				drawImgWithOpacity(plus_rs, (x + 60*s, y + 45*s + iconshift + chimera_shift * 2), plus_rs)
		if(type == 4):
			#mutation3
			displayMutation((x+20*s), (y+54*2) + chimera_shift * 3, mutation3, fill_c)
			if(mutation3[1: 3] == "el"):
				drawImgWithOpacity(minus_rs, (x + 60*s, y + 68*s + iconshift + chimera_shift * 3), minus_rs)
			else:
				if(mutation3[1: 3] == "ns"):
					drawImgWithOpacity(plus_rs, (x + 60*s, y + 68*s + iconshift + chimera_shift * 3), plus_rs)




for i in range(0, nsites):
	for j in range(0, nsamples):
		index = nsamples * 2 * i + j * 2
		x = 250 + i * 170
		y = 100 + j * 60 - 40
		mut1 = ""
		mut2 = ""
		mut3 = ""
		numreads = data["#Reads"][index]
		print("numreads:", numreads)

		# print("Notes:",data["NOTES"][index + 1][0:8])
		# if(data["NOTES"][index + 1][0:8] == "CHIMERA:"):
		# 	print("CHIMERA...")
		# 	mut3 = data["NOTES"][index + 1][8:13]

		if(data["n_deleted"][index] > 0):
			mut1 = "del" + str(data["n_deleted"][index])
		else:
			if (data["n_inserted"][index] > 0):
				if(data["n_inserted"][index] > 10):
					# this is caused from a faulty alignment! It is not realistic to have this much of an insertion
					mut1 = "No mut"
					mut1 = "ins" + str(data["n_inserted"][index])
				else:
					mut1 = "ins" + str(data["n_inserted"][index])
			else:
				mut1 = "No mut"

		if(data["n_deleted"][index + 1] > 0):
			mut2 = "del" + str(data["n_deleted"][index + 1])
		else:
			if (data["n_inserted"][index + 1] > 0):
				if(data["n_inserted"][index + 1] > 10):
					# this is caused from a faulty alignment! It is not realistic to have this much of an insertion
					mut2 = "No mut"
					mut2 = "ins" + str(data["n_inserted"][index + 1])
				else:
					mut2 = "ins" + str(data["n_inserted"][index + 1])
			else:
				mut2 = "No mut"


		if(data["n_mutated"][index] < 0):
			#special case, summarizer.cc marks as having no reads found
			mut1 = "no_reads"
			mut2 = "no_reads"

		fraction_first_mutation = data["%Reads"][index] / (data["%Reads"][index] + data["%Reads"][index + 1])
		# call >80% the first mutation a homozygote

		if(fraction_first_mutation > 0.8 or (mut1 == "No mut" and mut2 == "No mut") or (mut1 == "no_reads")):
			#homozygous
			if(mut1 == "no_reads"):
				displayCard(x * s, y * s, mut1, mut2, 0, numreads)
			else:
				if ((mut1 == "No mut")):
					displayCard(x * s, y * s, mut1, mut2, 0, numreads)
				else:
					displayCard(x * s, y * s, mut1, mut2, 1, numreads)

		else:
			# heterozygous
			if(mut1 == "No mut"):
				displayCard(x * s, y * s, mut1, mut2, 2, numreads)
			else:
				if (mut2 == "No mut"):
					displayCard(x * s, y * s, mut2, mut1, 2, numreads);
				else:
					if(mut3 == ""):
						displayCard(x * s, y*s, mut1, mut2, 3, numreads);
					else:
						displayCard(x * s, y*s, mut1, mut2, 4, numreads, mut3);
		
		

		if(i == 0):

			draw.text((s * 80, (y + 15) * s), str(data["Sample"][index]), fill = (0, 100, 0, 255), font = font_used)
			if "sal" in data["Sample"][index]:
				image.paste(sal_rs, (0, (y + 0) * s), sal_rs)
			elif "uc" in data["Sample"][index]:
				image.paste(uc_rs, (0, (y + 0) * s), uc_rs)
			elif "pi" in data["Sample"][index]:
				image.paste(pi_rs, (0, (y + 0) * s), pi_rs)

			elif "water" in data["Sample"][index] or "control" in data["Sample"][index] or "w" in data["Sample"][index]:
				image.paste(water_rs, (0, (y + 0) * s), water_rs)
				draw.text((s * 80, (y + 15) * s), data["Sample"][index], fill = (0, 25, 150, 255), font = font_used)
			elif RECQ4A_ver:
				image.paste(uc_rs, (0, (y + 0) * s), uc_rs)
				if(j == 0):
					image.paste(sal_rs, (10 * s, (y + 0) * s), sal_rs)
				if(j == 1):
					image.paste(pi_rs, (10 * s, (y + 0) * s), pi_rs)
			else:
				image.paste(default, (0, (y + 0) * s), default)


			if(j == 0):
				draw.text((s * 30, s * 25), "Sample", fill = (0, 100, 0, 255), font = font_used_big)
				draw.text((s * 150, s * 15), "Site", fill = (255, 141, 55, 255), font = font_used_big)

		if(j == 0):
			draw.text((x * s, 15 * s), str(sitenames[data["Site"][index] - 1]), fill = (255, 141, 55, 255), font = font_used_big)


image.save(sys.argv[1][:-4] + ".png", format = "PNG")

