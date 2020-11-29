import datetime
import functools #biblioteca dos decoradores

#Python básico
#stg = "a letra \"b\" está entre aspas"
#print(stg)


#set_1 = {1,2,3,4}

#print(type(set_1))
#print(set_1)

#Python avançado

print('List Comprehension')
[x for x in range(5)]

print([n for n in range(11) if n %2 == 1])

nome = ' vinicius '
print(nome.strip()) #retira espaço
print(nome.lower()) #minusculo
print(nome.upper()) #maiusculo
print(nome.strip().capitalize()) #primeira maiuscula

pessoas = ['AnA', ' FelIPE', 'vinicius ']

pessoas_ok = [pessoa.strip().capitalize() for pessoa in pessoas]
print(pessoas_ok)


#dicionarios
print('\nDicionarios')
dict1 = {'Nome': 'Ana', 'Idade' : 15}

list_dict = [{'Nome': 'Ana', 'Idade' : 15},
			 {'Nome': 'Vinicius', 'Idade' : 17},
			 {'Nome': 'Ronaldo', 'Idade' : 65}]

print(dict1)
print(list_dict[2])
print(list_dict[1]['Nome'])
print(list_dict[0]['Idade'])

loteria = {'Nome': 'Fulano', 'numeros': (1,25,36)} #tupla para nao ser alterada
print(loteria)
print(sum(loteria['numeros']))
loteria['Nome'] = 'Ana J'
print(loteria)

#objetos e classes
print('\nObjetos e Classes')
class JogadorLoteria:
	def __init__(self,nome, numeros): #self = ele mesmo (this)
		self.nome = nome
		self.numeros = numeros

	def total(self):
		return sum(self.numeros)

jogador_1 = JogadorLoteria('Ana', (1,2,3,4))
jogador_2 = JogadorLoteria('Vinicius', (1,2,3,4,5))

print(jogador_2.nome, jogador_2.numeros)
print(jogador_2.total())
print(jogador_1.nome, jogador_1.numeros)
print(jogador_1.total())


#Herança
print('\nHerança')
class Funcionario():
	def __init__(self, nome, salario):
		self.nome = nome
		self.salario = salario

	def dados(self):
		return {'nome': self.nome, 'salario': self.salario}


class Admin(Funcionario):
	def __init__(self, nome, salario):
		super().__init__(nome, salario) #chama o init do super

	def atualizar_dados(self, nome):
		self.nome = nome
		return self.dados()

#Funcionario
fabio = Funcionario('Fabio', 1560)
print(fabio.dados())

#Admin
fernando = Admin('Fernando', '3500')
print(fernando.dados())

fernando.atualizar_dados('Fernandinho')
print(fernando.dados())

#Metodos de classe e estaticos
print('\nMetodos de classe e Estáticos')
class FuncionarioTwo():
	aumento = 1.04

	def __init__(self, nome, salario): #SELF = proprio objeto
		self.nome = nome
		self.salario = salario

	def dados(self):
		return {'nome': self.nome, 'salario': self.salario}

	def aplicar_aumento(self):
		self.salario = self.salario * self.aumento

	@classmethod #metodo de classe, recebe CLS(propria classe)
	def definir_novo_aumento(cls, novo_aumento):
		cls.aumento = novo_aumento

	@staticmethod #metodo estatico, tem relação com a classe mas nao recebe nada da classe (self or cls)
	def dia_util(dia):
		#segunda = 0
		#domingo = 6
		if dia.weekday() == 5 or dia.weekday() == 6: #weekday gera o dia em numero 0-6
			return False #nao é dia util
		return True #é dia util

fabio2 = FuncionarioTwo('Fabio2', 1000)
antonio = FuncionarioTwo('Antonio', 1000)

#print(fabio2.dados())
fabio2.aplicar_aumento()
print(fabio2.dados())

FuncionarioTwo.definir_novo_aumento(1.05)
antonio.aplicar_aumento()
print(antonio.dados())

minha_data = datetime.date(2019, 4, 12) #quinta feira
print(FuncionarioTwo.dia_util(minha_data))

#Args e kwargs
print('\n*args e **kwargs')
#args = argumentos
#kwards = keyword arguments (argumentos de palavras-chave)

def meu_metodo(arg1, arg2):
	return arg1 + arg2

print(meu_metodo(5,6))

def meu_metodo_longo(arg1,arg2,arg3,arg4,arg5):
	return arg1+arg2+arg3+arg4+arg5

print(meu_metodo_longo(1,2,3,4,5))

def minha_lista_somada(lista):
	return sum(lista)

print(minha_lista_somada([1,2,3,5,6]))

def soma_simplificada(*args): #não se sabe qtos elementos irão vir(parecido com lista)
	return sum(args)

print(soma_simplificada(6,3,5,4,7))

def metodo_kwargs(*args, **kwargs):
	print(args)  #retorna como tupla
	print(args[3]) 
	print(kwargs) #retorna como dict
	print(kwargs['idade'])

#args antes dos kwargs SEMPRE
#sem argumento é ARGS / com argumento é KWARGS
metodo_kwargs(3, 'saa', 4, 'qualquer', nome='ana', idade=25)

#Decoradores
print('\nDecoradores')

def meu_decorador(funcao):
	@functools.wraps(funcao) #embrulhar
	def func_que_roda_funcao():
		print("*****Embrulhando função no decorador!*******")
		funcao()
		print("******Fechando embrulho********")
	return func_que_roda_funcao

@meu_decorador
def minha_funcao():
	print("Eu sou uma função!")

minha_funcao()
