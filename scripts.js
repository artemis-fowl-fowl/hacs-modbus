var ModbusServer = 'http://192.168.1.11:2080/';

//var ModbusServer = 'http://moulin427.myds.me:2080/';		// Redirig� sur 192.168.1.11:2080 par la box

//var ModbusServer = 'https://modbus.moulin427.myds.me/';		// Redirigé via reverse proxy

//var ModbusServer = 'http://home.moulin427.myds.me:2081/';		// Redirigé via reverse proxy

//var ModbusServer = 'http://moulin427.myds.me:81/';		// Redirig� sur 192.168.1.21:80 par la box
//var ModbusServer = 'http://arduino.moulin427.myds.me/';		// Redirig� sur 192.168.1.21:80 par le reverse proxy du NAS


var temp;
var link=false;
var blink=0;
var trameBrute = "[0,0,0,0,0][0,0,0,0,0][0,0,0,0,0]";

/*
RAF:
*!!!!!!!!!!!!!!!Modifier la fa�on dont est g�r� l'appel � drawPage.
Le script envoie facilement des trames writeCoil erron�es au serveur, et en plus le serveur plante sur l'instruction trame=list(map(int,msg_recu[i+1:j].split(',')));

Si le serveur ne r�pond pas les requetes sembles m�moris�es en empil�es de sorte qu'au retour du serveur celui-ci re�oit une salve. A r�soudre.
*/

function bascule(elem) {
	etat=document.getElementById(elem).style.display;
	if(etat=="none") {
		document.getElementById(elem).style.display="block";
	}
	else {
		document.getElementById(elem).style.display="none";
	}
}

function single(id, label, device, index, switchAddr) {
    this.id = id;                   // Load point id as it will appear in the htlm file
    this.label = label;             // Load point label
    this.device = device;           // Modbus device (slave address - 1)
    this.index = index;             // Output position in the automate (0 = Q1 ... 8 = Q7 ... 9 = Y1 ... 15 = Y8) 
    this.switchAddr = switchAddr;   // Input coil address that can switch the load point (with Modbus function 05; see table 4.11 of ismart MODBUS guide)
    this.state = -1;                 // Load point state (0 = OFF; 1 = ON; -1 = Erreur)
}

function volet(id, label, device, index, downAddr, scenario) {
    this.id = id;               // VR id as it will appear in the html file
    this.label = label;         // VR label
    this.device = device;       // Modbus device (slave address - 1)
    this.index = index;         // Output position in the automate (0 = Q1 ... 15 = Y8) 
    this.downAddr = downAddr;   // Input coil address that can switch down the VR (with Modbus function 05; see table 4.11 of ismart MODBUS guide)
    this.upAddr = downAddr+1;
	this.state = 0;             // VR state (0:Ind�termin� 1:Ouvert 2:Ferm� 3:En ouverture 4:En fermeture -1: Erreur)
	this.scenario = scenario;	// Etat du volet dans les sc�narios 1 (soleil)
}


function portail(id, label, device, switchAddr) {
    this.id = id;               	// Portail id as it will appear in the html file
	this.device = device;	     	// Modbus device (slave address - 1)
    this.label = label;         	// label
    this.switchAddr = switchAddr;   // Input coil address that can open / stop / close the door (with Modbus function 05; see table 4.11 of ismart MODBUS guide)	
	this.state = 0;             	// state (0:Ind�termin� 1:Ouvert 2:Ferm� 3:En fonctionnement 4:V�rouill� ouvert -1: Erreur)
}

function alarm(id, label, device, switchAddr,) {
    this.id = id;               	// Alarme id as it will appear in the html file
	this.device = device;	       	// Modbus device (slave address - 1)
    this.label = label;         	// label
    this.switchAddr = switchAddr;   // Input coil address that can engage / dis-engage the alarme (with Modbus function 05; see table 4.11 of ismart MODBUS guide)
	this.state = 0;             	// state (0:Ind�termin� 1:Standby 2:Arm�e 3:En Alarme -1: Erreur)
}

function scenario(id, label) {
    this.id = id;               // Scenario id as it will appear in the html file
    this.label = label;         // Scenario label
	this.state = 0;             // VR state (0:Non r�alis� 1:R�alis� -1: Erreur)	
}

var single = [
    new single('sParents','Parents',1,0,0x2C00),
    new single('sDressing','Dressing',1,1,0x2C01),
    new single('sGabriel','Gabriel',1,2,0x2C02),
    new single('sPaul','Paul',1,3,0x2C03),
    new single('sSophie','Sophie',1,4,0x2C04),
    new single('sSDB','SDB',1,5,0x2C05,2),
    new single('sMiroir_SDB','Miroir',1,6,0x2C06),
    new single('sDouche','Douche',1,7,0x2C07),
    new single('sGrenier','Grenier',1,8,0x2C10),
    new single('sCouloir','Couloir',1,9,0x2C11),
    new single('sMezz','Mezzanine',1,10,0x2C12),
    new single('sSejour','Sejour',1,11,0x2C13),
    new single('sPasserelle','Passerelle',1,12,0x2C14),
    new single('sCabanon','Cabanon',1,13,0x2C15),
    new single('sSDJ','SDJ',1,14,0x2C16),
    new single('sWC_ET','WC',1,15,0x2C17),
    new single('sSalon1','Salon 1',2,0,0x2C00),
    new single('sSalon2','Salon 2',2,1,0x2C01),
    new single('sCuisine','Cuisine',2,2,0x2C02),
    new single('sIlot','Ilot',2,3,0x2C03),
    new single('sEvier','Evier',2,4,0x2C04),
    new single('sTerrasse','Terrasse',2,5,0x2C05),
    new single('sBuanderie','Buanderie',2,6,0x2C06),
    new single('sMiroir_B','Miroir',2,7,0x2C07),
    new single('sWC_RDC','WC',2,8,0x2C10),
    new single('sHall','Hall',2,9,0x2C11),
    new single('sCellier','Cellier',2,10,0x2C12),
    new single('sAtelier','Atelier',2,11,0x2C13),
    new single('sPreau','Preau',2,12,0x2C14),
    new single('sGarage','Garage',2,13,0x2C15),
    new single('sCave','Cave',2,14,0x2C16),
    new single('sCour','Cour',2,15,0x2C17),
    new single('sLit_Aurel','Lit Aurel',3,14,0x2C16),
    new single('sLit_Aline','Lit Aline',3,15,0x2C17),
    new single('sSejour.A','Sejour.A',4,10,0x2C12),
    new single('sSejour.B','Sejour.B',4,11,0x2C13),
    new single('sLit_Gabriel','Lit_Gabriel',4,12,0x2C14),
    new single('sLit_Paul','Lit Paul',4,13,0x2C15),
    new single('sLit_Sophie','Lit Sophie',4,14,0x2C16),
    new single('sRadSDB','RadSDB',5,6,0x2C06),
    new single('sSalon.A','Apoint',5,0,0x2C00),
    new single('sSalon.B','Ampli',5,1,0x2C01),
	// Hack: J'utiliser pour accéder au memstate les valeurs à partir de 100
	new single('sArrosageAuto','Arrosage auto',5,109,0x0549),		// 109 = M0A; 0x0549 = M0A
    new single('sArrosageZ1','Arrosage Zone1',5,2,0x2C02),
    new single('sArrosageZ2','Arrosage Zone2',5,3,0x2C03),
    new single('sPriseCharge','Prise charge Scooter',5,107,0x0547),	// 107 = M08; 0x0547 = M08
    new single('sBorneCharge','Borne charge VE',5,108,0x0548),		// 108 = M09; 0x0548 = M09
];					

var alarm = [
    new alarm('sAlarme','Alarme',5,0x2C09),				// 0x2C09 = X01
];

var portail = [
    new portail('pCour','Portail cour',5,0x2C13),		// 0x2C13 = X04
    new portail('pGarage','Garage',5,0x2C04),			// 0x2C04 = I5
];

var volet = [
    new volet('vrParents','Parents',3,0,0x2C00,[2,2]),
    new volet('vrGabriel','Gabriel',3,2,0x2C02,[2,2]),
    new volet('vrPaul.W','Paul.W',3,4,0x2C04,[2,2]),
    new volet('vrPaul.S','Paul.S',3,6,0x2C06,[2,0]),
    new volet('vrSophie','Sophie',3,8,0x2C10,[2,0]),
    new volet('vrMezz','Mezzanine',3,10,0x2C12,[2,0]),
    new volet('vrVelux','Velux',3,12,0x2C14,[1,2]),
    new volet('vrCath','Cathedra.',4,0,0x2C00,[1,0]),
    new volet('vrBua','Buanderie',4,2,0x2C02,[2,0]),
    new volet('vrCuisine','Cuisine',4,4,0x2C04,[2,0]),
    new volet('vrSejour.W','Sejour.W',4,6,0x2C06,[2,2]),
    new volet('vrSejour.S','Sejour.S',4,8,0x2C10,[1,0]),
    new volet('vrEscalier','Escalier',4,10,0x2C12,[1,0]),	
    new volet('vrEtage','Etage',3,0,0x2C08,[0,0]),              	// Index ne correspond � rien
    new volet('vrRDC','RDC',4,0,0x2C08,[0,0]),          	      	// Index ne correspond � rien
    new volet('vrGeneral','General',4,0,0x2C08,[0,0]),	            // Device et index ne correspondent � rien    
];

var scenario = [
	new scenario('scSoleil','Soleil'),
	new scenario('scOmbre','Ombre'),
//	new scenario('scOFF','OFF'),
//	new scenario('scBynight,'OFF'),
];

/* Envoie une requette vers le serveur TCP puis attend l'�tat des automates en r�ponse */
function sendServer(cmd)
{
	var i;
    $.ajaxSetup({timeout:2000});                // Ajax requests timeout
	$.get(ModbusServer + cmd)					// Utilisation de jquery
        .done(function(trameBrute)			// D�finition de la fonction execut�e apr�s le succ�s -> Attention, c'est asynchrone!!!
		{
            $('#trame_brute').html("trameBrute: "+trameBrute);
			trameBrute = trameBrute.replaceAll('][',';');
			trameBrute = trameBrute.replace('[','');
			trameBrute = trameBrute.replace(']','');
			lists = trameBrute.split(";");
    // Il faut analyser la trame et d�tecter si elle est mauvaise. Il faudra peut �tre mettre un code de d�tection d'erreur.
	
            validState = (lists[0].split(","));
			outState = (lists[1].split(","));
			memState = (lists[2].split(","));
            $('#outstate_list').html("outState: "+outState);
		    $('#outvalid_list').html("validState: "+validState);
            $('#memstate_list').html("memState: "+memState);	
			
        // On la r�partition suivante: [0]:Automate1.Q, [1]:Automate1.Y, [2]:Automate2.Q, [3]:Automate2.Y, [4]:Automate3.Q, [5]:Automate3.Y
        //                             [6]:Automate4.Q, [7]:Automate4.Y, [8]:Automate5.Q, [9]:Automate5.Y
			link=true;							// Le flag link indique que la connexion avec le serveur fonctionne

			decodeState();
			drawPage();							// Dessine les �l�ments javascript
        })
    .fail(function() 
	{						// D�finition de la fonction execut�e apr�s �chec -> Attention, c'est asynchrone!!!
		link=false;							// Le flag link indique que la connexion ne fonctionne pas
        // !!!!!!!!!!!!!!!!!!TBC!!!!!!!!!!!!!!!!!!
		drawPage();							// Dessine les �l�ments javascript
    });
}

function decodeState() {
	var i;
	// Etat des sorties single: 0:OFF 1:ON -1:Erreur
    for (var i in single) {
		if (validState[single[i].device-1]==0) single[i].state=-1;			                    // La donn�e lue pour cette sortie n'est pas valide
		else if ((single[i].index < 100) && (outState[single[i].device-1] & (0x1 << single[i].index)) == 0) single[i].state=0;	// La donn�e lue pour cette sortie est "0"
		// Hack pour lire en memState les index à partir de 100
		else if ((single[i].index > 99) && (memState[single[i].device-1] & (0x1 << (single[i].index-100))) == 0) single[i].state=0;
		else single[i].state=1;										                            // La donn�e lue pour cette sortie est "1"
	}

	// Etat alarme
	if (validState[alarm[0].device-1]==0) alarm[0].state=-1;				                    // La donn�e lue pour cette sortie n'est pas valide
	else if (memState[alarm[0].device-1]&(0x1<<4)) alarm[0].state=3;							// Alarme arm�e (M05 = Alarme active)
	else if (memState[alarm[0].device-1]&(0x1<<3)) alarm[0].state=2;							// Alarme arm�e (M04 = Arm�e)
	else alarm[0].state=1;																		// Alarme en standby			
	
	// Etat portail cours
	portail[0].state=0
	if (validState[portail[0].device-1]==0) portail[0].state=-1;			                    // La donn�e lue pour cette sortie n'est pas valide
	else if (memState[portail[0].device-1]&(0x1<<0)) portail[0].state=3;						// Portail en fonctionnement (M01 = RUN)
	else if (memState[portail[0].device-1]&(0x1<<1)) portail[0].state=2;						// Portail ferm� (M02 = CLOSED)
	else if (memState[portail[0].device-1]&(0x1<<2)) portail[0].state=4;						// Portail v�rouill� (M03 = LOCKED)
	else portail[0].state=1;

	// Etat porte garage
	portail[1].state=0
	if (validState[portail[1].device-1]==0) portail[1].state=-1;			                    // La donn�e lue pour cette sortie n'est pas valide
	else if (memState[portail[1].device-1]&(0x1<<5)) portail[1].state=1;						// Portail ouvert (M06 = OUVERT)
	else if (memState[portail[1].device-1]&(0x1<<6)) portail[1].state=2;						// Portail ferm� (M07 = FERME)
	else portail[1].state=3;																	// Portail en fonctionnement (ni ouvert ni ferm�)

		
	
	// Etat des sorties VR: 0:Ind�termin� 1:Ouvert 2:Ferm� 3:En ouverture 4:En fermeture -1:Erreur
//	for (var i in volet) {
	for (i=0; i<13; i++) {
		if (!validState[volet[i].device-1]) volet[i].state=-1;			                        // La donn�e lue pour cette sortie n'est pas valide
		else if (outState[volet[i].device-1]&(0x1<<volet[i].index)) volet[i].state=4;		    // Le volet est en cours de fermeture
        else if (outState[volet[i].device-1]&(0x1<<(volet[i].index+1))) volet[i].state=3;		// Le volet est en cours d'ouverture
		else if (memState[volet[i].device-1]&(0x1<<volet[i].index)) volet[i].state=2;		    // Le volet est ferm�
        else if (memState[volet[i].device-1]&(0x1<<(volet[i].index+1))) volet[i].state=1;		// Le volet est ouvert
		else volet[i].state=0;										                            // L'�tat du volet est ind�termin�
	}

    // Contruction de l'�tat du groupe de volet �tage
    volet[13].state=volet[0].state
	for (i=1; i<7; i++) {
		if (volet[13].state!=volet[i].state) volet[13].state=0;	// On regarde si tous les volet de l'�tage sont dans le m�me �tat sinon l'�tat du groupe est ind�termin�
	}    

    // Contruction de l'�tat du groupe de volet RDC
    volet[14].state=volet[7].state
	for (i=8; i<14; i++) {
		if (volet[14].state!=volet[i].state) volet[14].state=0;	// On regarde si tous les volet de l'�tage sont dans le m�me �tat sinon l'�tat du groupe est ind�termin�
	}    

    // Construction de l'�tat du groupe de volet G�n�ral	    
	if (volet[13].state!=volet[14].state) volet[15].state=0;		// On regarde si tous les volet sont dans le m�me �tat sinon l'�tat du groupe est ind�termin�
	else volet[15].state=volet[13].state;

	// Construction de l'�tat des scenarios
	//for (var i in scenario)		// V�rifier si cette fonction fonctionne
	for (j=0; j<2; j++) {				// remplacer par une fonction qui parcours le tableau
		scenario[j].state=1
		for (i=0; i<11; i++) {		// remplacer par une fonction qui parcours le tableau
			if (volet[i].state!=volet[i].scenario[j]) scenario[j].state=0;		// On regarde si tous les volets sont dans l'�tat correspondant au sc�nario1
						// Touver comment faire passer un index dans pour avoir volet[i].scenario[j]
		}
	}
}


function drawPage() {
	toggleBlink();
			if (blink==0) document.getElementById('B1').innerHTML = "blink";		
			else document.getElementById('B1').innerHTML = "\n";		
	
	// Affiche le statut de la connexion
	if (link==0) document.getElementById('C1').innerHTML = "Connexion: KO";
	else document.getElementById('C1').innerHTML = "Connexion: OK";

	// Affiche les informations de d�buggage

	for (var i in single) {				// Affichage des boutons pour les points lumineux
		if (single[i].state==0)
			document.getElementById(single[i].id).innerHTML = "<input type='button' class='OFF' name='S"+i+"' onClick='toggle("+i+")' value='OFF' /> <label for'S"+i+"'>"+single[i].label+"</label>";
		else if (single[i].state==1)
			document.getElementById(single[i].id).innerHTML = "<input type='button' class='ON' name='S"+i+"' onClick='toggle("+i+")' value='ON' /> <label for'S"+i+"'>"+single[i].label+"</label>";
		else
			document.getElementById(single[i].id).innerHTML = "<input type='button' class='UNKNOWN' name='S"+i+"' value='-' /> <label for'S"+i+"'>"+single[i].label+"</label>";
	}
	
	for (var i in alarm) {				// Affichage des boutons pour l'alarm
		if (alarm[i].state==0)			// Etat inconnu		
			document.getElementById(alarm[i].id).innerHTML = "<input type='button' class='UNKNOWN' name='S"+i+"' onClick='togglealarm("+i+")' value='-' /> <label for'S"+i+"'>"+alarm[i].label+"</label>";
		else if (alarm[i].state==1)			// Alarme en standby			
			document.getElementById(alarm[i].id).innerHTML = "<input type='button' class='OFF' name='S"+i+"' onClick='togglealarm("+i+")' value='OFF' /> <label for'S"+i+"'>"+alarm[i].label+"</label>";
		else if (alarm[i].state==2)		// Alarme arm�e
			document.getElementById(alarm[i].id).innerHTML = "<input type='button' class='ON' name='S"+i+"' onClick='togglealarm("+i+")' value='ON' /> <label for'S"+i+"'>"+alarm[i].label+"</label>";
		else if (alarm[i].state==3) {	// En alarme
			if (blink==0) document.getElementById(alarm[i].id).innerHTML = "<input type='button' class='ON' name='S"+i+"' onClick='togglealarm("+i+")' value='!!' /> <label for'S"+i+"'>"+alarm[i].label+"</label>";
			else document.getElementById(volet[i].id).innerHTML = "<input type='button' class='RUN' name='S"+i+"' onClick='togglealarm("+i+")' value='O' /> <label for'S"+i+"'>"+alarm[i].label+"</label>";		
			}
		else							//
			document.getElementById(alarm[i].id).innerHTML = "<input type='button' class='UNKNOWN' name='S"+i+"' value='!' /> <label for'S"+i+"'>"+alarm[i].label+"</label>";
	}	
	
	for (var i in volet) {				// Affichage des boutons pour les volet roulants et groupes de volets roulants
		if (volet[i].state==0)				// Position ind�termin�e
			document.getElementById(volet[i].id).innerHTML = "<input type='button' class='VR UNKNOWN' name='VRup"+i+"' onClick='upVR("+i+")' value='UP' /> <input type='button' class='VR UNKNOWN' name='VRdown"+i+"' onClick='downVR("+i+")' value='DO' /> <label for'VR"+i+"'>"+volet[i].label+"</label>";
		else if (volet[i].state==1)				// volet ouvert
			document.getElementById(volet[i].id).innerHTML = "<input type='button' class='VR ON' name='VRup"+i+"' onClick='upVR("+i+")' value='UP' /> <input type='button' class='VR OFF' name='VRdown"+i+"' onClick='downVR("+i+")' value='DO' /> <label for'VR"+i+"'>"+volet[i].label+"</label>";
		else if (volet[i].state==2)			// volet ferm�
			document.getElementById(volet[i].id).innerHTML = "<input type='button' class='VR OFF' name='VRup"+i+"' onClick='upVR("+i+")' value='UP' /> <input type='button' class='VR ON' name='VRdown"+i+"' onClick='downVR("+i+")' value='DO' /> <label for'VR"+i+"'>"+volet[i].label+"</label>";		
		else if (volet[i].state==3) {		// volet en cours d'ouverture
			if (blink==0) document.getElementById(volet[i].id).innerHTML = "<input type='button' class='VR OFF' name='VRup"+i+"' onClick='upVR("+i+")' value='UP' /> <input type='button' class='VR OFF' name='VRdown"+i+"' onClick='downVR("+i+")' value='DO' /> <label for'VR"+i+"'>"+volet[i].label+"</label>";		
			else document.getElementById(volet[i].id).innerHTML = "<input type='button' class='VR RUN' name='VRup"+i+"' onClick='upVR("+i+")' value='UP' /> <input type='button' class='VR OFF' name='VRdown"+i+"' onClick='downVR("+i+")' value='DO' /> <label for'VR"+i+"'>"+volet[i].label+"</label>";		
			}
		else if (volet[i].state==4) {		// volet en cours de fermeture
			if (blink==0) document.getElementById(volet[i].id).innerHTML = "<input type='button' class='VR OFF' name='VRup"+i+"' onClick='upVR("+i+")' value='UP' /> <input type='button' class='VR OFF' name='VRdown"+i+"' onClick='downVR("+i+")' value='DO' /> <label for'VR"+i+"'>"+volet[i].label+"</label>";		
			else document.getElementById(volet[i].id).innerHTML = "<input type='button' class='VR OFF' name='VRup"+i+"' onClick='upVR("+i+")' value='UP' /> <input type='button' class='VR RUN' name='VRdown"+i+"' onClick='downVR("+i+")' value='DO' /> <label for'VR"+i+"'>"+volet[i].label+"</label>";		
			}		
		else							// Valeur non lue (erreur)
			document.getElementById(volet[i].id).innerHTML = "<input type='button' class='VR UNKNOWN' name='VRup"+i+"' value='!' /> <input type='button' class='VR UNKNOWN' name='VRdown"+i+"' value='!' /> <label for'VR"+i+"'>"+volet[i].label+"</label>";
	}

	for (var i in portail) {				// Affichage des boutons pour les portails
		if (portail[i].state==0)				// Position ind�termin�e
			document.getElementById(portail[i].id).innerHTML = "<input type='button' class='UNKNOW' name='P"+i+"' onClick='toggleportail("+i+")' value='-' /> <label for'P"+i+"'>"+portail[i].label+"</label>";
		else if (portail[i].state==1)			// portail ouvert
			document.getElementById(portail[i].id).innerHTML = "<input type='button' class='ON' name='P"+i+"' onClick='toggleportail("+i+")' value='OPEN' /> <label for'P"+i+"'>"+portail[i].label+"</label>";
		else if (portail[i].state==2)			// portail ferm�
			document.getElementById(portail[i].id).innerHTML = "<input type='button' class='OFF' name='P"+i+"' onClick='toggleportail("+i+")' value='CLOSE' /> <label for'P"+i+"'>"+portail[i].label+"</label>";	
		else if (portail[i].state==3) {			// portail en mouvement
			if (blink==0) 			document.getElementById(portail[i].id).innerHTML = "<input type='button' class='ON' name='P"+i+"' onClick='toggleportail("+i+")' value='RUN' /> <label for'P"+i+"'>"+portail[i].label+"</label>";
			else document.getElementById(portail[i].id).innerHTML = "<input type='button' class='RUN' name='P"+i+"' onClick='toggleportail("+i+")' value='RUN' /> <label for'P"+i+"'>"+portail[i].label+"</label>";		
			}
		else if (portail[i].state==4)			// portail v�rouill�
		document.getElementById(portail[i].id).innerHTML = "<input type='button' class='RUN' name='P"+i+"' onClick='toggleportail("+i+")' value='LOCK' /> <label for'P"+i+"'>"+portail[i].label+"</label>";		
		else							// Valeur non lue (erreur)
			document.getElementById(portail[i].id).innerHTML = "<input type='button' class='ERROR' name='P"+i+"' onClick='toggleportail("+i+")' value='!' /> <label for'P"+i+"'>"+portail[i].label+"</label>";		
	}
	
	for (var i in scenario) {				// Affichage des boutons pour les scenarios
		if (scenario[i].state==0)
			document.getElementById(scenario[i].id).innerHTML = "<input type='button' class='OFF' name='SC"+i+"' onClick='doscenario("+i+")' value='OFF' /> <label for'SC"+i+"'>"+scenario[i].label+"</label>";
		else if (scenario[i].state==1)
			document.getElementById(scenario[i].id).innerHTML = "<input type='button' class='ON' name='SC"+i+"' onClick='doscenario("+i+")' value='ON' /> <label for'SC"+i+"'>"+scenario[i].label+"</label>";
		else
			document.getElementById(scenario[i].id).innerHTML = "<input type='button' class='UNKNOWN' name='SC"+i+"' value='-' /> <label for'SC"+i+"'>"+scenario[i].label+"</label>";
	}
}
	
function doscenario(j) {
	for (var j in scenario) {
		for (i=0; i<11; i++) {			// remplacer par une fonction qui parcours le tableau
			if (volet[i].scenario[j]==1)	upVR(i)			// On ouvre les volets qui doivent l'�tre dans le scenario
			if (volet[i].scenario[j]==2)	downVR(i)		// On ferme les volets qui doivent l'�tre dans le scenario
						// Touver comment faire passer un index dans pour avoir volet[i].scenario[j]
		}
	}
}
	
function toggleportail(i) {
    sendServer('writeCoil['+portail[i].device+','+portail[i].switchAddr+','+1+']');
}

function toggle(i) {
	// Hack pour faire une ON/OFF au lieu d'un pulse si l'index est supérieur à 100 (ce qui n'a pas forcément de lien mais qui fonctionne dans le cas de l'arrosage auto)
	if (single[i].index > 99 && single[i].state == 1)
		sendServer('writeCoil['+single[i].device+','+single[i].switchAddr+','+0+']');
    else sendServer('writeCoil['+single[i].device+','+single[i].switchAddr+','+1+']');
}

function togglealarm(i) {
    sendServer('writeCoil['+alarm[i].device+','+alarm[i].switchAddr+','+1+']');
}

function downVR(i) {
    if (i==14) {    // General
        sendServer('writeCoil['+volet[i].device+','+volet[13].downAddr+','+1+']');
    }
    else sendServer('writeCoil['+volet[i].device+','+volet[i].downAddr+','+1+']');
}

function upVR(i) {
    sendServer('writeCoil['+volet[i].device+','+volet[i].upAddr+','+1+']');
}

function generalUpVR(){
	upVR(12);		// Commande g�n�rale up VR �tage
	upVR(13);       // Commande g�n�rale up VR RDC
}

function generalDownVR(){
	downVR(12);		// Commande g�n�rale down VR �tage
	downVR(13);     // Commande g�n�rale down VR RDC	
}

function toggleBlink(){
	if (blink==0) blink=1;
	else blink=0;
}

// Dessine les �lements javascript au lancement de la page
$(document).ready(function() {
//	sendServer('getState');								// Actualise la page
	setInterval("sendServer('getState')", 2000);		// Actualise l'�tat des automates toutes les 2 secondes
	//Peut �tre mettre un timeout pour �viter la connection perp�tuelle.
});

/*
	function clignotte(obj){
		var timer = setInterval(function(){obj.style.visibility = (obj.style.visibility=='visible')?'hidden':'visible';},500);
		setTimeout("clearInterval(timer);",5000);
	}
*/
