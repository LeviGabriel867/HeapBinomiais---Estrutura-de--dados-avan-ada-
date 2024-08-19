class BinomialHeapNode:
    def __init__(self, key, patient_id):
        self.key = key  # Prioridade do paciente
        self.patient_id = patient_id  # ID do paciente
        self.parent = None
        self.child = None
        self.sibling = None
        self.degree = 0

    def __str__(self):
        return f"Paciente {self.patient_id} com prioridade {self.key}"

    def print_node(self, level=0):
        # Imprime o nó atual e os filhos (usado para debug se necessário)
        print(' ' * level * 2, f"Paciente {self.patient_id} com prioridade {self.key}")
        if self.child:
            self.child.print_node(level + 1)
        if self.sibling:
            self.sibling.print_node(level)

class BinomialHeapNode:
    def __init__(self, key, patient_id):
        self.key = key  # Prioridade do paciente
        self.patient_id = patient_id  # ID do paciente
        self.parent = None
        self.child = None
        self.sibling = None
        self.degree = 0

    def __str__(self):
        return f"Paciente ID: {self.patient_id}, Prioridade: {self.key}"

    def __repr__(self):
        return self.__str__()


class BinomialHeap:
    def __init__(self):
        self.head = None

    def merge(self, h1, h2):
        if not h1:
            return h2
        if not h2:
            return h1

        # Mescla as duas listas de raízes ordenadas por grau
        if h1.degree <= h2.degree:
            h1.sibling = self.merge(h1.sibling, h2)
            return h1
        else:
            h2.sibling = self.merge(h1, h2.sibling)
            return h2


    def union(self, other_heap):
        if not self.head:
            return other_heap
        if not other_heap.head:
            return self

        # Mesclar as duas listas de raízes
        new_heap = BinomialHeap()
        new_heap.head = self.merge(self.head, other_heap.head)

        if not new_heap.head:
            return None

        prev = None
        current = new_heap.head
        next = current.sibling

        while next:
            if (current.degree != next.degree) or (next.sibling and next.sibling.degree == current.degree):
                prev = current
                current = next
            else:
                if current.key <= next.key:
                    current.sibling = next.sibling
                    self.link(next, current)
                else:
                    if not prev:
                        new_heap.head = next
                    else:
                        prev.sibling = next
                    self.link(current, next)
                    current = next
            next = current.sibling

        return new_heap 

    def link(self, y, z):
        y.parent = z
        y.sibling = z.child
        z.child = y
        z.degree += 1

    def insert(self, node):
        new_heap = BinomialHeap()
        new_heap.head = node
        self.head = self.union(new_heap).head

    def extract_min(self):
        if not self.head:
            return None

        prev_min = None
        min_node = self.head
        prev = None
        current = self.head

        while current.sibling:
            if current.sibling.key < min_node.key:
                prev_min = current
                min_node = current.sibling
            current = current.sibling

        if prev_min:
            prev_min.sibling = min_node.sibling
        else:
            self.head = min_node.sibling

        child = min_node.child
        new_heap = BinomialHeap()

        while child:
            next = child.sibling
            child.sibling = new_heap.head
            new_heap.head = child
            child = next

        self.head = self.union(new_heap).head
        return min_node


class Consultorio:
    def __init__(self, id):
        self.id = id
        self.fila_prioritaria = BinomialHeap()
        self.fila_nao_prioritaria = BinomialHeap()

    def inserir_paciente(self, prioridade, patient_id, prioritario):
        new_node = BinomialHeapNode(prioridade, patient_id)
        if prioritario:
            print(f"Inserindo paciente prioritário {patient_id} na fila do consultório {self.id}")
            self.fila_prioritaria.insert(new_node)
        else:
            print(f"Inserindo paciente não prioritário {patient_id} na fila do consultório {self.id}")
            self.fila_nao_prioritaria.insert(new_node)


    def atender_paciente(self):
        if self.fila_prioritaria.head:
            return self.fila_prioritaria.extract_min()
        elif self.fila_nao_prioritaria.head:
            return self.fila_nao_prioritaria.extract_min()
        return None

class CentralHospitalar:
    def __init__(self):
        # Inicializa a central hospitalar com três consultórios
        self.consultorios = {1: Consultorio(1), 2: Consultorio(2), 3: Consultorio(3)}
        self.historico = []

    def chegada_paciente(self, prioridade, patient_id, consultorio_id, prioritario):
        # Verifica se o consultório existe
        if consultorio_id in self.consultorios:
            # Adiciona o paciente na fila correta
            self.consultorios[consultorio_id].inserir_paciente(prioridade, patient_id, prioritario)
            # Registra no histórico
            self.historico.append(f"INC {'P' if prioritario else 'N'} {prioridade} - {consultorio_id}")
        else:
            # Mensagem de erro se o consultório não existir
            print(f"Erro: O consultório {consultorio_id} não existe. Por favor, adicione o paciente em um consultório existente.")

    def atendimento_paciente(self, consultorio_id):
        # Verifica se o consultório existe
        if consultorio_id in self.consultorios:
            consultorio = self.consultorios[consultorio_id]
            paciente_atendido = consultorio.atender_paciente()
            if paciente_atendido:
                # Registra no histórico
                self.historico.append(f"ATT {paciente_atendido.patient_id} - {consultorio_id}")
            else:
                print(f"Consultório {consultorio_id} não tem pacientes para atender.")
        else:
            print(f"Erro: O consultório {consultorio_id} não existe.")

    def abrir_consultorio(self, consultorio_id):
        # Abre um novo consultório, se não existir ainda
        if consultorio_id not in self.consultorios:
            self.consultorios[consultorio_id] = Consultorio(consultorio_id)
            print(f"Consultório {consultorio_id} foi aberto.")
        else:
            print(f"Consultório {consultorio_id} já está aberto.")

    def fechar_consultorio(self, consultorio_id):
        # Fecha um consultório e redistribui seus pacientes
        if consultorio_id in self.consultorios:
            if len(self.consultorios) > 3:
                consultorio = self.consultorios.pop(consultorio_id)
                self.redistribuir_pacientes(consultorio)
                print(f"Consultório {consultorio_id} foi fechado e os pacientes foram redistribuídos.")
            else:
                print("Erro: Não é possível fechar o consultório. Devem permanecer pelo menos três consultórios abertos.")
        else:
            print(f"Erro: O consultório {consultorio_id} não existe.")

    def redistribuir_pacientes(self, consultorio):
        for id, other_consultorio in self.consultorios.items():
            # Redistribuindo pacientes prioritários
            while consultorio.fila_prioritaria.head:
                node = consultorio.fila_prioritaria.extract_min()
                if isinstance(node, BinomialHeapNode):
                    print(f"Redistribuindo paciente prioritário {node.patient_id} do consultório fechado para o consultório {id}")
                    other_consultorio.inserir_paciente(node.key, node.patient_id, True)
                else:
                    print("Erro: O nó extraído não é um BinomialHeapNode.")
        
        # Redistribuindo pacientes não prioritários
        while consultorio.fila_nao_prioritaria.head:
            node = consultorio.fila_nao_prioritaria.extract_min()
            if isinstance(node, BinomialHeapNode):
                print(f"Redistribuindo paciente não prioritário {node.patient_id} do consultório fechado para o consultório {id}")
                other_consultorio.inserir_paciente(node.key, node.patient_id, False)
            else:
                print("Erro: O nó extraído não é um BinomialHeapNode.")



    def exibir_status(self):
        # Exibe o status de todos os consultórios
        print("Status dos Consultórios:")
        for id, consultorio in self.consultorios.items():
            print(f"\nConsultório {id}:")
            
            # Mostrar fila prioritária
            if consultorio.fila_prioritaria.head:
                print("  Fila Prioritária:")
                self._print_fila(consultorio.fila_prioritaria.head)
            else:
                print("  Fila Prioritária: Vazia")
            
            # Mostrar fila não prioritária
            if consultorio.fila_nao_prioritaria.head:
                print("  Fila Não Prioritária:")
                self._print_fila(consultorio.fila_nao_prioritaria.head)
            else:
                print("  Fila Não Prioritária: Vazia")

    def _print_fila(self, node):
        # Auxilia na impressão das filas
        while node:
            print(f"    {node}")
            node = node.sibling
    def gerar_historico(self):
        with open('historico.txt', 'w') as file:
            for entry in self.historico:
                file.write(entry + "\n")
        print("Histórico salvo em historico.txt.")



def main():
    central = CentralHospitalar()
    while True:
        print("\nMenu:")
        print("1. Chegada de um novo paciente")
        print("2. Atendimento de um paciente")
        print("3. Abertura de um novo consultório")
        print("4. Fechamento de um consultório")
        print("5. Exibir status dos consultórios")
        print("6. Sair e salvar histórico")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            prioridade = int(input("Prioridade do paciente: "))
            patient_id = int(input("ID do paciente: "))
            consultorio_id = int(input("ID do consultório: "))
            prioritario = input("Paciente prioritário (S/N): ").strip().upper() == 'S'
            central.chegada_paciente(prioridade, patient_id, consultorio_id, prioritario)
        elif opcao == "2":
            consultorio_id = int(input("ID do consultório para atendimento: "))
            central.atendimento_paciente(consultorio_id)

        elif opcao == "3":
            consultorio_id = int(input("ID do consultório a ser aberto: "))
            central.abrir_consultorio(consultorio_id)
        elif opcao == "4":
            consultorio_id = int(input("ID do consultório a ser fechado: "))
            central.fechar_consultorio(consultorio_id)
        elif opcao == "5":
            central.exibir_status()
        elif opcao == "6":
            central.gerar_historico()

            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
