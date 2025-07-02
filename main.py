# backend/main.py
import os
from tabulate import tabulate
from services.crud_usuario import (
    listar_usuarios,
    criar_usuario,
    listar_bairros,
    criar_bairro,
    listar_ocorrencias,
    criar_ocorrencia,
    buscar_ocorrencias_por_categoria,
    atualizar_ocorrencia,
    deletar_ocorrencia,
    exportar_ocorrencias_json
)
from services.utils import validar_data
from ui import (
    console, linha, painel, menu, input_pastel,
    sucesso, erro, alerta, info, pause, loading_fake
)
from logger import log_info, log_sucesso, log_erro, log_alerta


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_principal():
    while True:
        clear_screen()
        painel("Bem-vindo ao ELO!", titulo="ELO")
        opcoes = [
            "Listar usuários",
            "Criar usuário",
            "Listar bairros",
            "Criar bairro",
            "Listar ocorrências",
            "Criar ocorrência",
            "Buscar ocorrências por categoria",
            "Atualizar ocorrência",
            "Deletar ocorrência",
            "Exportar ocorrências para JSON"
        ]
        escolha = menu("Menu Principal", opcoes)

        if not escolha.isdigit():
            erro("Opção inválida (digite um número). Tente novamente.")
            log_alerta("Usuário digitou opção não numérica no menu principal.")
            pause()
            continue

        opc = int(escolha)

        if opc == 0:
            info("Saindo... Até mais!")
            log_info("Usuário encerrou o programa.")
            break

        elif opc == 1:
            log_info("Usuário escolheu listar usuários.")
            loading_fake("Carregando usuários...")
            usuarios = listar_usuarios()
            if usuarios:
                console.print(tabulate(usuarios, headers="keys", tablefmt="fancy_grid"))
            else:
                alerta("Nenhum usuário encontrado.")
                log_alerta("Nenhum usuário cadastrado ao listar usuários.")
            pause()

        elif opc == 2:
            log_info("Usuário escolheu criar usuário.")
            painel("Criar novo usuário", titulo="Novo Usuário")
            nome = input_pastel("Nome")
            papel = input_pastel("Papel (prefeitura, ong, admin)")
            email = input_pastel("E-mail")
            try:
                novo_id = criar_usuario(nome, papel, email)
                sucesso(f"Usuário criado com ID {novo_id}")
                log_sucesso(f"Usuário criado: ID {novo_id}, Nome: {nome}, Papel: {papel}, Email: {email}")
            except Exception as e:
                erro(f"Erro ao criar usuário: {e}")
                log_erro(f"Erro ao criar usuário: {e}")
            pause()

        elif opc == 3:
            log_info("Usuário escolheu listar bairros.")
            loading_fake("Carregando bairros...")
            bairros = listar_bairros()
            if bairros:
                console.print(tabulate(bairros, headers="keys", tablefmt="fancy_grid"))
            else:
                alerta("Nenhum bairro encontrado.")
                log_alerta("Nenhum bairro cadastrado ao listar bairros.")
            pause()

        elif opc == 4:
            log_info("Usuário escolheu criar bairro.")
            painel("Criar novo bairro", titulo="Novo Bairro")
            nome = input_pastel("Nome do Bairro")
            try:
                area_risco_prop = float(input_pastel("Proporção de área de risco (0.0 a 1.0)").replace(",", "."))
            except ValueError:
                erro("Valor inválido para proporção de área de risco.")
                log_erro("Valor inválido para proporção de área de risco ao criar bairro.")
                pause()
                continue
            try:
                pop_densidade = float(input_pastel("Densidade populacional (habitantes/km²)").replace(",", "."))
            except ValueError:
                erro("Valor inválido para densidade populacional.")
                log_erro("Valor inválido para densidade populacional ao criar bairro.")
                pause()
                continue
            try:
                novo_id = criar_bairro(nome, area_risco_prop, pop_densidade)
                sucesso(f"Bairro criado com ID {novo_id}")
                log_sucesso(f"Bairro criado: ID {novo_id}, Nome: {nome}")
            except Exception as e:
                erro(f"Erro ao criar bairro: {e}")
                log_erro(f"Erro ao criar bairro: {e}")
            pause()

        elif opc == 5:
            log_info("Usuário escolheu listar ocorrências.")
            loading_fake("Carregando ocorrências...")
            ocorrencias = listar_ocorrencias()
            if ocorrencias:
                console.print(tabulate(ocorrencias, headers="keys", tablefmt="fancy_grid"))
            else:
                alerta("Nenhuma ocorrência encontrada.")
                log_alerta("Nenhuma ocorrência cadastrada ao listar ocorrências.")
            pause()

        elif opc == 6:
            log_info("Usuário escolheu criar ocorrência.")
            painel("Criar nova ocorrência", titulo="Nova Ocorrência")
            titulo_oc = input_pastel("Título")
            descricao = input_pastel("Descrição")
            categoria = input_pastel("Categoria (ex: alagamento, deslizamento)")
            data = input_pastel("Data (YYYY-MM-DD)")
            if not validar_data("%Y-%m-%d", data):
                erro("Formato de data inválido. Use YYYY-MM-DD.")
                log_erro("Data inválida ao criar ocorrência.")
                pause()
                continue
            status = input_pastel("Status (ex: aberta, em andamento, encerrada)")
            localizacao = input_pastel("Localização (descrição ou ponto de referência)")
            try:
                usuario_id = int(input_pastel("ID do Usuário responsável"))
                bairro_id = int(input_pastel("ID do Bairro afetado"))
            except ValueError:
                erro("ID inválido. Deve ser um número inteiro.")
                log_erro("ID inválido ao criar ocorrência.")
                pause()
                continue
            try:
                novo_id = criar_ocorrencia(
                    titulo_oc, descricao, categoria, data, status, localizacao, usuario_id, bairro_id
                )
                sucesso(f"Ocorrência criada com ID {novo_id}")
                log_sucesso(f"Ocorrência criada: ID {novo_id}, Título: {titulo_oc}")
            except Exception as e:
                erro(f"Erro ao criar ocorrência: {e}")
                log_erro(f"Erro ao criar ocorrência: {e}")
            pause()

        elif opc == 7:
            log_info("Usuário escolheu buscar ocorrências por categoria.")
            painel("Buscar ocorrências por categoria", titulo="Buscar Ocorrências")
            categoria = input_pastel("Categoria")
            resultados = buscar_ocorrencias_por_categoria(categoria)
            if resultados:
                console.print(tabulate(resultados, headers="keys", tablefmt="fancy_grid"))
            else:
                alerta(f"Nenhuma ocorrência encontrada na categoria '{categoria}'.")
                log_alerta(f"Nenhuma ocorrência encontrada na categoria '{categoria}'.")
            pause()

        elif opc == 8:
            log_info("Usuário escolheu atualizar ocorrência.")
            painel("Atualizar ocorrência existente", titulo="Atualizar Ocorrência")
            try:
                id_oc = int(input_pastel("ID da ocorrência a ser atualizada"))
            except ValueError:
                erro("ID inválido. Deve ser um número inteiro.")
                log_erro("ID inválido ao atualizar ocorrência.")
                pause()
                continue
            campo = input_pastel(
                "Campo para atualizar (titulo, descricao, categoria, data, status, localizacao)"
            ).lower()
            if campo not in {"titulo", "descricao", "categoria", "data", "status", "localizacao"}:
                erro("Campo inválido ou não permitido.")
                log_erro("Campo inválido ao atualizar ocorrência.")
                pause()
                continue
            valor = input_pastel("Novo valor")
            if campo == "data" and not validar_data("%Y-%m-%d", valor):
                erro("Formato de data inválido. Use YYYY-MM-DD.")
                log_erro("Data inválida ao atualizar ocorrência.")
                pause()
                continue
            sucesso_update = atualizar_ocorrencia(id_oc, {campo: valor})
            if sucesso_update:
                sucesso(f"Ocorrência {id_oc} atualizada com sucesso.")
                log_sucesso(f"Ocorrência atualizada: ID {id_oc}, Campo: {campo}, Novo Valor: {valor}")
            else:
                erro("Ocorrência não encontrada.")
                log_erro(f"Tentativa de atualizar ocorrência não encontrada: ID {id_oc}")
            pause()

        elif opc == 9:
            log_info("Usuário escolheu deletar ocorrência.")
            painel("Deletar ocorrência existente", titulo="Deletar Ocorrência")
            try:
                id_oc = int(input_pastel("ID da ocorrência a ser deletada"))
            except ValueError:
                erro("ID inválido. Deve ser um número inteiro.")
                log_erro("ID inválido ao deletar ocorrência.")
                pause()
                continue
            sucesso_delete = deletar_ocorrencia(id_oc)
            if sucesso_delete:
                sucesso(f"Ocorrência {id_oc} deletada com sucesso.")
                log_sucesso(f"Ocorrência deletada: ID {id_oc}")
            else:
                erro("Ocorrência não encontrada.")
                log_erro(f"Tentativa de deletar ocorrência não encontrada: ID {id_oc}")
            pause()

        elif opc == 10:
            log_info("Usuário escolheu exportar ocorrências para JSON.")
            painel("Exportar ocorrências para JSON", titulo="Exportar")
            try:
                exportar_ocorrencias_json()
                sucesso("Exportado para ./export/ocorrencias_export.json")
                log_sucesso("Exportação de ocorrências para JSON realizada.")
            except Exception as e:
                erro(f"Erro na exportação: {e}")
                log_erro(f"Erro na exportação de ocorrências para JSON: {e}")
            pause()

        else:
            erro("Opção inválida. Digite um número entre 0 e 10.")
            log_alerta(f"Opção inválida no menu principal: {escolha}")
            pause()

    info("Programa encerrado.")
    log_info("Programa encerrado pelo usuário.")


if __name__ == "__main__":
    menu_principal()