# include <GFButton.h>

GFButton botaoC(44);
GFButton botaoCs(42);
GFButton botaoD(40);
GFButton botaoDs(38);
GFButton botaoE(36);
GFButton botaoF(34);
GFButton botaoFs(32);
GFButton botaoG(30);
GFButton botaoGs(28);
GFButton botaoA(26);
GFButton botaoAs(24);
GFButton botaoB(22);

GFButton botao[12] = {botaoC, botaoCs, botaoD,botaoDs, botaoE, botaoF, botaoFs, botaoG, botaoGs, botaoA, botaoAs, botaoB};

int rledC = 53;
int rledCs = 51;
int rledD = 49;
int rledDs = 47;
int rledE = 45;
int rledF = 43;
int rledFs = 41;
int rledG = 39;
int rledGs = 37;
int rledA = 35;
int rledAs = 33;
int rledB = 31;

int gledC = 2;
int gledCs = 3;
int gledD = 4;
int gledDs = 5;
int gledE = 6;
int gledF = 7;
int gledFs = 8;
int gledG = 9;
int gledGs = 10;
int gledA = 11;
int gledAs = 12;
int gledB = 13;

int ledsred[12] = {rledC, rledCs, rledD, rledDs, rledE, rledF, rledFs, rledG, rledGs, rledA, rledAs, rledB};
int ledsgreen[12] = {gledC, gledCs, gledD, gledDs, gledE, gledF, gledFs, gledG, gledGs, gledA, gledAs, gledB};

String arrayAnterior = "";
unsigned long estadoInativo = 0;
const unsigned long estadoIntervalo = 20;

unsigned long tempoInativo[12] = {0};
const unsigned long intervalo = 150;
bool verifica = false;

void processarNota(String nota) {
  int notaInt = nota.toInt();
  if (notaInt != 0) {
    int notaEsperada = abs(notaInt);
    bool acenderVerde = (notaInt > 0);

    if (notaEsperada >= 1 && notaEsperada <= 12) {
      if (acenderVerde) {
        digitalWrite(ledsgreen[notaEsperada - 1], HIGH);
      } else {
        digitalWrite(ledsred[notaEsperada - 1], HIGH);
      }
      tempoInativo[notaEsperada - 1] = millis();
    }
  }
}

void setup() {
Serial.begin(4800);
for(int i = 0; i < 12; i++){
 pinMode(ledsred[i], OUTPUT);
 digitalWrite(ledsred[i], LOW);
 pinMode(ledsgreen[i], OUTPUT);
 digitalWrite(ledsgreen[i], LOW);
}
}

void loop() {
  String botoesPressionados = "";
  for (int i = 0; i < 12; i++) {
    botao[i].process();

    if (botao[i].isPressed()){
      digitalWrite(ledsred[i], HIGH);
      if (botoesPressionados.length() > 0) {
        botoesPressionados += ",";
      }
      botoesPressionados += String(i + 1);
    }
    else if(millis() - estadoInativo >= estadoIntervalo){
      digitalWrite(ledsred[i], LOW);
    }
  }

  if (millis() - estadoInativo >= estadoIntervalo) {
    if(botoesPressionados != arrayAnterior){
      if (botoesPressionados.length() > 0) {
        Serial.println("[" + botoesPressionados + "]");
        verifica = true;
      }
      if (botoesPressionados.length() == 0){
        if(verifica){
          Serial.println("[]");
          verifica = false;
        }
      }
    arrayAnterior = botoesPressionados;
    }
    estadoInativo = millis();
  }

  if (Serial.available() > 0) {
    String texto = Serial.readStringUntil('\n');
    if (texto[0] == '[' && texto[texto.length() - 1] == ']') {
      texto = texto.substring(1, texto.length() - 1);
      int index = 0;
      String nota;
      while (index < texto.length()) {
        char currentChar = texto[index];
        if (currentChar == ',') {
          processarNota(nota);
          nota = "";
        } else {
          nota += currentChar;
        }
        index++;
      }
      if (nota.length() > 0) {
        processarNota(nota);
      }
    }
  }

  for (int i = 0; i < 12; i++) {
    if (millis() - tempoInativo[i] > intervalo) {
      digitalWrite(ledsred[i], LOW);
      digitalWrite(ledsgreen[i], LOW);
    }
  }
}