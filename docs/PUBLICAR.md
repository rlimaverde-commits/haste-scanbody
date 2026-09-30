# Como publicar no GitHub e gerar o DOI no Zenodo

Tempo estimado: 20–30 minutos. Faça nesta ordem: o Zenodo só gera o DOI a partir de uma *release* do GitHub criada **depois** de ligar a integração.

## 1. Antes de publicar

- [ ] Atualize `D_SCANBODY` com a medida real e regenere os STL (`python3 src/haste_scanbody.py stl`).
- [ ] Confira nome e afiliação em `LICENSE`, `LICENSE-MODELS.md`, `CITATION.cff` e `.zenodo.json`.
- [ ] Se tiver ORCID, preencha em `CITATION.cff` e acrescente `"orcid": "0000-..."` no criador em `.zenodo.json`.

## 2. Criar o repositório no GitHub

1. Entre em https://github.com (crie uma conta, se não tiver).
2. Clique em **New repository**.
    - Nome: `haste-scanbody`
    - Visibilidade: **Public** (o Zenodo só arquiva repositórios públicos).
    - **Não** marque "Add a README", "Add .gitignore" nem "Choose a license": esses arquivos já estão no pacote.
3. Na página do repositório vazio, clique em **uploading an existing file**.
4. Descompacte o `haste-scanbody.zip` no seu computador e arraste **todo o conteúdo da pasta** (não a pasta em si) para a janela.
    - Os arquivos `.gitignore` e `.zenodo.json` começam com ponto e podem ficar ocultos. No macOS, `Cmd + Shift + .` mostra os ocultos no Finder; no Windows, ative "Itens ocultos" no Explorador.
5. Mensagem do commit: `Versão inicial 1.0.0`. Clique em **Commit changes**.
6. Confira se as pastas `stl/`, `src/`, `docs/`, `img/` e os arquivos `.zenodo.json` e `CITATION.cff` aparecem.

## 3. Ligar o Zenodo ao GitHub

1. Entre em https://zenodo.org e clique em **Log in → Log in with GitHub**. Autorize o acesso.
2. No menu do usuário, abra **GitHub**.
3. Clique em **Sync now** e ative a chave (ON) ao lado de `haste-scanbody`.

## 4. Criar a release (gera o DOI)

1. No GitHub, no repositório, clique em **Releases → Create a new release**.
2. **Choose a tag:** digite `v1.0.0` e clique em "Create new tag".
3. **Release title:** `v1.0.0 — versão inicial`.
4. Descrição sugerida: "Primeira versão pública: 4 hastes codificadas (A–D), gerador paramétrico e instruções de impressão e uso."
5. Clique em **Publish release**.
6. Em alguns minutos o Zenodo arquiva a versão. Em https://zenodo.org, no menu **GitHub**, aparece o **DOI** ao lado do repositório.

O Zenodo cria dois DOIs:
- **Concept DOI:** aponta sempre para a versão mais recente. Use este no artigo.
- **Version DOI:** aponta só para a v1.0.0.

## 5. Depois do DOI

1. Copie o selo (badge) do DOI que o Zenodo oferece e cole no topo do `README.md`.
2. Substitua `[DOI]` e `[URL do GitHub]` no `README.md`, no cabeçalho de `src/haste_scanbody.py` e em `CITATION.cff` (descomente as linhas `doi` e `repository-code`).
3. Faça o commit dessas alterações pelo próprio site do GitHub (ícone de lápis em cada arquivo).
4. No manuscrito, preencha a declaração de disponibilidade de dados e código com a URL e o DOI.

## Novas versões

Quando alterar o desenho (por exemplo, após o caso clínico), crie uma nova release (`v1.1.0`). O Zenodo gera um novo DOI de versão automaticamente e mantém o anterior.
