from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton
from PyQt5.uic import loadUi
import sys
import pickle


class Enigma(QMainWindow):
    def __init__(self):
        super(Enigma , self).__init__()
        loadUi("enigma.ui" , self)
        
        self.rotor_1 = ''
        self.rotor_beta_1 = ''
        
        self.rotor_2 = ''
        self.rotor_beta_2 = ''
        
        self.rotor_3 = ''
        self.rotor_beta_3 = ''
        
        self.result = self.findChild(QTextEdit , 'result')
        self.txt = self.findChild(QLineEdit , 'input')
        self.bcs = self.findChild(QPushButton, 'bcs')
        self.txt = self.findChild(QTextEdit , 'txt')
        
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.num = '1234567890'
        
        self.cipher = ''
        self.plain = ''
        
        self.rotate_counter = 0
        self.unrotate_counter = 0
        
        self.Setting()
        
        self.input.textChanged['QString'].connect(self.Get_Char)
        self.input.textChanged['QString'].connect(self.input.clear)
        self.input.returnPressed.connect(self.Next_Line)
        self.bcs.clicked.connect(self.Dell)
    
    
    
    
    
    def Setting(self):
        with open(sys.argv[1], 'rb') as setting:
            self.rotor_1, self.rotor_beta_1, self.rotor_2, self.rotor_beta_2, self.rotor_3, self.rotor_beta_3 = pickle.load(setting)
          
          
            
    
    def Get_Char(self):
        char = self.input.text()
        
        if char != '' and char in self.alphabet:
            self.rotate_counter += 1
            self.plain += char
            self.Encode_Alpha((char, 'l'))
            
        elif char != '' and char in self.alphabet_upper:
            self.rotate_counter += 1
            self.plain += char
            self.Encode_Alpha((char, 'u'))
        
        elif char != '' and char in self.num:
            self.rotate_counter += 1
            self.plain += char
            self.Encode_Beta(char)
            
        elif char == ' ' or char not in self.alphabet:
            self.plain += char
            self.Make_Text(char)
        
       
       
       
        
    def Reflector(self, char):
        if char in self.alphabet:
            return self.alphabet[len(self.alphabet)-self.alphabet.index(char)-1] 
         
        elif char in self.num:
            return self.num[len(self.num)-self.num.index(char)-1] 
    
    
    
    
    
    def Encode_Beta(self, char):
        index = self.num.index(char)
        c1 = self.rotor_beta_1[index]
        
        index = self.num.index(c1)
        c2 = self.rotor_beta_2[index]
        
        index = self.num.index(c2)
        c3 = self.rotor_beta_3[index]
        
        r = self.Reflector(c3)
        
        index = self.rotor_beta_3.index(r)
        c3 = self.num[index]
        
        index = self.rotor_beta_2.index(c3)
        c2 = self.num[index]
        
        index = self.rotor_beta_1.index(c2)
        char= self.num[index]
        
        self.Make_Text(char)
        self.Rotate()
    
    
    
    
    
    
    def Encode_Alpha(self, char):
        char_lower = char[0].lower()
        
        index = self.alphabet.index(char_lower)
        c1 = self.rotor_1[index]
        
        index = self.alphabet.index(c1)
        c2 = self.rotor_2[index]
        
        index = self.alphabet.index(c2)
        c3 = self.rotor_3[index]
        
        r = self.Reflector(c3)
        
        index = self.rotor_3.index(r)
        c3 = self.alphabet[index]
        
        index = self.rotor_2.index(c3)
        c2 = self.alphabet[index]
        
        index = self.rotor_1.index(c2)
        c1= self.alphabet[index]
        
        if char[1] == 'u':
            c1 = c1.upper()
        
        self.Make_Text(c1)
        self.Rotate()




        
    def Rotate(self):
        self.rotor_1 = self.rotor_1[1:] + self.rotor_1[0]
        
        if self.rotate_counter % 26 == 0:
            self.rotor_2 = self.rotor_2[1:] + self.rotor_2[0]
            if self.rotate_counter  % (26*26) == 0:
                self.rotor_3 = self.rotor_3[1:] + self.rotor_3[0]

    
    
    
    
    def Make_Text(self, char):
        self.cipher += char
        self.Write()




        
    def Next_Line(self):
        self.plain += '\n'
        self.Make_Text('\n')




        
    def Dell(self):
        self.cipher = self.cipher[:-1]
        self.plain = self.plain[:-1]
        self.unrotate_counter -= 1
        self.Unrotate()
        self.Write()

    
    
    
    
    def Unrotate(self):
        self.rotor_1 = self.rotor_1[-1] + self.rotor_1[:-1]
        
        if self.unrotate_counter % 26 == 0:
            self.rotor_2 = self.rotor_2[-1] + self.rotor_2[:-1]
            if self.unrotate_counter  % (26*26) == 0:
                self.rotor_3 = self.rotor_3[-1] + self.rotor_3[:-1]

    
    
    
    
    def Write(self):
        self.result.setText(self.cipher)
        self.txt.setText(self.plain)
        self._File()





    def _File(self):
        with open('Message.txt', 'w') as file:
            file.write(self.cipher)


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Enigma()
    window.show()
    sys.exit(app.exec_())
