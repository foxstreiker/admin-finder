import shelve
import urllib2
import sys
import httplib
import socket
from urllib2 import Request, urlopen, URLError, HTTPError
red	= 	"\033[01;31m"
green = 	"\033[01;32m"
yel =		"\033[01;33m"
norm	=	"\033[0m" 

def controllo():
	try:
		f=open("links_db","r")
		f.close()
	except IOError :
		print "%sFile links_db inesistente %s" %(red,norm)
		sys.exit()
		
def carica():
	link_S=[]
	db=shelve.open("links_db")
	if not db["0"]:
		print "File non presente o file vuoto"
	else :
		link_S=db["0"]
	db.close()
	return link_S

def salva(link_S):
	db=shelve.open("links_db")
	db["0"]=link_S
	db.close()
	
	
def visualizza():
	link_S=carica()
	for i in range(len(link_S)):
		print link_S[i]


def aggiungi (pagina): 
	link_S=carica()	
	if not pagina:
		try :
			linkFile=raw_input("\nInserire nome del file txt (es. link.txt) \n=> ")
			f=open(linkFile,"r")
			while True :
				link=f.readline()
				if not link.strip():
					break
				if link.strip() in link_S :
					print "\nLink %s %s %s gia' presente" %(red,link.strip(),norm)				
				if link.strip() not in link_S :	
					link_S.append(link.strip())
					print "\n link %s %s %s aggiunto con successo" % (green,link.strip(),norm)
							
			f.close()			
		except IOError :
			print "File %s %s %s inesistente " %(red,linkFile,norm)				
				
		
	else :
		if pagina in link_S:	
			link_S.append(pagina)
			print "\nLink %s %s %s gia' presente" %(red,pagina,norm)		
		if pagina not in link_S:	
			link_S.append(pagina)
			print "\nLink %s %s %s aggiunto con successo" %(green,pagina,norm)
	salva(link_S)
	return link_S
				


def v_link(link):
	link=link.replace("https://","")
	link=link.replace("http://","")
	if "/" in link :
		ind = link.find("/")
		link=link[:ind]
	return link
			
def AdminFind2(link,link_S):
	link=v_link(link)
	conn = httplib.HTTPConnection(link)
	conn.request("GET","")
	stat=conn.getresponse()
	if stat.status != 200:
		print "%sSito offline o URL non valido%s" %(red,norm)
	else :
		for pag in link_S:
			if pag[0] != "/":
				pag="/"+pag
			conn = httplib.HTTPConnection(link)
			conn.request("GET",pag)
			stat=conn.getresponse()
			sys.stdout.write('\r'+"Scanning %s" %(link+pag))
			sys.stdout.flush()
			if stat.status == 200 :
				print "\nPossible  => %s %s %s"% (green,link+pag,norm)
		
def credit():
	print '''
	%s
	AdminFinder by Maxstreiker 
	https://github.com/maxstreiker/
	%s
	'''% (yel,norm)







if __name__=="__main__":
	controllo()
	credit()
	link_S=carica()
	while True:
		print ''' 
		Ci sono %s pagine 
		Inserire :
		1) per cercare la pagina 
		2) per aggiungere la/e pagina/e
		3) visualizzare le pagine 
		0) per uscire
		''' % len(link_S)
		risp=raw_input("=>  ")
		if risp=="1": 
			link=raw_input("\nInserire URL del sito : es. www.example.com \n=>   ")
			AdminFind2(link,link_S)
		elif risp=="2":
			pagina=raw_input("\nInserire la pagina da aggiungere es. admin.php o premere invio per inserire una lista di pagine dal file link.txt \n=>")
			link_S=aggiungi(pagina)
		elif risp=="3":
			visualizza()
		elif risp=="0":
			sys.exit()
		else :
			print "%s Errore %s " %(red,norm)
			
	




