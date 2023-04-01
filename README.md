# <p align = "center"> API - 1° Semestre - Banco de Dados 2023 
<p/>

<p align = "center">
<img src= "https://user-images.githubusercontent.com/111469327/229311756-7adfe563-68ab-42d2-99c1-948d5f3b7f0e.jpg" width="650" height="300"/>

<p align = "center">
   
## 📍 Sumário

 * [Projeto API](#projeto_API)
    * [Apresentação da Equipe](#apresentação-da-equipe)
    * [Integrantes](#integrantes)
    * [Tema](#tema)
    * [Objetivo](#objetivo)
    * [Planejamento de entregas](#planejamento-de-entregas)
 * [Produto DEVTUDO](#produto_DEVTUDO)
    * [Preview da plataforma](#preview-da-plataforma)
    * [Arquitetura do Projeto](#arquitetura-do-projeto)
    * [Backlog do produto](#backlog-do-produto)
    * [Tecnologias ultilizadas](#tecnologias-ultilizadas)
    * [Ferramentas ultilizadas](#ferramentas-ultilizadas)
    
    
##
# Projeto API

## Apresentação da Equipe
  
Equipe composta por jovens programadores engajados a aprender e solucionar problemas complexos no decorrer do processo.  
Nosso objetivo é automatizar um produto de forma que cada passo seja validado pelo(a) cliente e/ou usuários, promovendo a evolução do serviço organicamente.

## :mortar_board: Integrantes
   
| NOME | ATRIBUIÇÃO | REDES SOCIAIS    | IDENTIFICAÇÃO |
| -----| ---------- | -------------    | ------------- |  
| Renan  | Scrum Master  | [<img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white"/>](https://www.linkedin.com/in/renan-graciano-faria-76134324b) [<img src="https://camo.githubusercontent.com/fbc3df79ffe1a99e482b154b29262ecbb10d6ee4ed22faa82683aa653d72c4e1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769744875622d3130303030303f7374796c653d666f722d7468652d6261646765266c6f676f3d676974687562266c6f676f436f6c6f723d7768697465" />](https://github.com/VonNexx)
| Beatriz| Product Owner | [<img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white"/>](https://www.linkedin.com/in/beatrizzpl%C3%A1cido) [<img src="https://camo.githubusercontent.com/fbc3df79ffe1a99e482b154b29262ecbb10d6ee4ed22faa82683aa653d72c4e1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769744875622d3130303030303f7374796c653d666f722d7468652d6261646765266c6f676f3d676974687562266c6f676f436f6c6f723d7768697465" />](https://github.com/BeatrizPlacido) | <img src="https://media.licdn.com/dms/image/D4D03AQHq83d7nitsAg/profile-displayphoto-shrink_800_800/0/1680134212385?e=1685577600&v=beta&t=5rBrdz9Id6ia0-10fOCjfKAb4VEIpek1cplGM9Atpes" height="60"/>
| Thomas | Desenvolvedor | [<img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white"/>](https://www.linkedin.com/in/thomas-cavalheiro-13250953) [<img src="https://camo.githubusercontent.com/fbc3df79ffe1a99e482b154b29262ecbb10d6ee4ed22faa82683aa653d72c4e1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769744875622d3130303030303f7374796c653d666f722d7468652d6261646765266c6f676f3d676974687562266c6f676f436f6c6f723d7768697465" />](https://github.com/Thomastrc) | <img src="https://avatars.githubusercontent.com/u/127264350?v=4" height="60"/>
| Ingrid | Desenvolvedor | [<img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white"/>](https://www.linkedin.com/in/ingridkaneko/) [<img src="https://camo.githubusercontent.com/fbc3df79ffe1a99e482b154b29262ecbb10d6ee4ed22faa82683aa653d72c4e1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769744875622d3130303030303f7374796c653d666f722d7468652d6261646765266c6f676f3d676974687562266c6f676f436f6c6f723d7768697465" />](https://github.com/KanekoIngrid) | <img src="https://media.licdn.com/dms/image/D4D03AQH9BVSRlqjZEw/profile-displayphoto-shrink_800_800/0/1664943454804?e=1685577600&v=beta&t=_1u-J8lFjuuBlLtYUPsZtE-1LDPEogXzRx8OGnRgQlQ" height="60"/>
| João   | Desenvolvedor | [<img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white"/>](https://www.linkedin.com/in/joao-saldanha/) [<img src="https://camo.githubusercontent.com/fbc3df79ffe1a99e482b154b29262ecbb10d6ee4ed22faa82683aa653d72c4e1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769744875622d3130303030303f7374796c653d666f722d7468652d6261646765266c6f676f3d676974687562266c6f676f436f6c6f723d7768697465" />](https://github.com/joa0-saldanha)| <img src="https://avatars.githubusercontent.com/u/80000631?v=4" height="60"/>
| Luis   | Desenvolvedor | [<img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white"/>](https://www.linkedin.com/in/luis-guimar%C3%A3es-99865b1b8) [<img src="https://camo.githubusercontent.com/fbc3df79ffe1a99e482b154b29262ecbb10d6ee4ed22faa82683aa653d72c4e1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769744875622d3130303030303f7374796c653d666f722d7468652d6261646765266c6f676f3d676974687562266c6f676f436f6c6f723d7768697465" />](https://github.com/LuisPGuimaraes) | <img src = "https://media.licdn.com/dms/image/D4D03AQECO_2qmDz9zw/profile-displayphoto-shrink_800_800/0/1680297083327?e=1685577600&v=beta&t=RrRZuEdDkettHZbDETp-dwE0VbmbCGyTgGmWTNLtKvU" height="60"/>
| Mariana | Desenvolvedor | [<img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" />](https://www.linkedin.com/in/marianac%C3%A1ssia/) [<img src = "https://camo.githubusercontent.com/fbc3df79ffe1a99e482b154b29262ecbb10d6ee4ed22faa82683aa653d72c4e1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769744875622d3130303030303f7374796c653d666f722d7468652d6261646765266c6f676f3d676974687562266c6f676f436f6c6f723d7768697465" />](https://github.com/Mcsalme) | <img src = "https://avatars.githubusercontent.com/u/111469327?v=4" height="60"/>
| Yuri   | Desenvolvedor | [<img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white"/>](https://br.linkedin.com/in/yuri-carmo-andrade-5b760910b) [<img src="https://camo.githubusercontent.com/fbc3df79ffe1a99e482b154b29262ecbb10d6ee4ed22faa82683aa653d72c4e1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769744875622d3130303030303f7374796c653d666f722d7468652d6261646765266c6f676f3d676974687562266c6f676f436f6c6f723d7768697465" />](https://github.com/yca2036) | <img src = "https://media.licdn.com/dms/image/C4D03AQHb4sPxA2S7uA/profile-displayphoto-shrink_800_800/0/1637316788504?e=1685577600&v=beta&t=VxnmIgquOLzq0kXM9B_eBw_ikFFWZ7uj0KqAh3SFD-c" height="60"/>
   
## Tema

>  Desenvolvimento de uma solução computacional que viabilize a aplicação da técnica de **Avaliação 360°** obtendo o resultado das análises dos dados pelos alunos e   instrutores da instituição de ensino PBLTeX especializada em cursos e práticas de ensino. 

## Objetivo

> - A aplicação (no projeto) de técnicas de programação para a construção de algoritmos
> - O uso de uma ferramenta que possibilite um Ambiente de Desenvolvimento Integrado (IDE) para o desenvolvimento da solução computacional
> - O aprendizado e aplicação de uma ou mais linguagens de programação para concepção do projeto
> - O exercício do compromisso, responsabilidade e trabalho em equipe dos membros do Time (sucesso / fracasso de TODOS)


## :date: Planejamento de Entregas 

> - [x] 13/02 a 03/03 - Kick-off
> - [x] 13/03 a 02/04 - Sprint 01
> - [x] 03/04 a 23/04 - Sprint 02
> - [x] 24/04 a 14/05 - Sprint 03
> - [x] 15/05 a 04/06 - Sprint 04
> - [x] 13/06 a 14/06 - Feira de soluções

##
# Produto DEVTUDO

## Preview da plataforma
+ #### (AGUARDANDO ANEXO VIDEO PROTOPIPO)

   
## Arquitetura do Projeto

Disponivel pelo [Figma](https://www.figma.com/file/86VvL8DaM6IR9RH06jVobp/PBLTeX-Projeto?node-id=0%3A1&t=Av9utODXTrCT0tAK-1)
   
## :date: Backlog do Produto
   
> - [x] Entrega da documetação do projeto e plataforma GITHUB
> - [x] 13/03 a 02/04 - Sprint 01
> - [x] 03/04 a 23/04 - Sprint 02
> - [x] 24/04 a 14/05 - Sprint 03
> - [x] 15/05 a 04/06 - Sprint 04
> - [x] 13/06 a 14/06 - Feira de soluções

## :computer: Tecnologias ultilizadas

<div style="display: inline_block"><br>
  <img align="center" alt="David-Js" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-plain.svg">
  <img align="center" alt="David-HTML" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg">
  <img align="center" alt="David-CSS" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original.svg">
  <img align="center" alt="David-Python" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">
  
 <div style="display: inline_block"><br>
   
## Ferramentas ultilizadas

<div style="display: inline_block"><br>
 
  <img align="center" alt="David-figma" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/figma/figma-original.svg" />
  <img align="center" alt="David-Canvas" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/canva/canva-original.svg" />
  <img align="center" alt="David-Github" height="40" width="40" src="https://pngimg.com/uploads/github/github_PNG51.png" />
  <img align="center" alt="David-Vscode" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg" />
  <img align="center" alt="David-Wp" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/wordpress/wordpress-original.svg" />
 <div style="display: inline_block"><br>
