#PROJETO FINAL - ALGORITMOS DE AUTOMAÇÃO
## Insper - 1T/24

Projeto final desenvolvido para a disciplina de Algoritmos de Automação, ministrada pelo professor Álvaro Justen pelo curso de Jornalismo de Dados, Automação e Datastorytelling do Insper.

O [site](https://projeto-final-aa.onrender.com) está no ar através da plataforma Render, onde foram criadas variáveis de ambiente necessárias para o site, mas sem expôr credenciais ou informações como e-mails, por exemplo.

O site contém 4 páginas: [home]([https://aa.onrender.com/), [portfólio](https://aa-pf.onrender.co](https://aa-pf.onrender.com)m/portfolio), [currículo](https://aa-pf.onrender.com/curriculo), [Manchetes DW](https://aa-pf.onrender.com/dw). As três primeiras correspondem ao portfólio da jornalista Ana Carolina Andrade, etapa inicial do projeto, desenvolvida em grupo. A quarta página corresponde à segunda etapa, que consistia na elaboração de um html dinâmico. Para isso, foi criado um raspador da página [Manchetes](https://www.dw.com/pt-br/manchetes/headlines-pt-br) do portal Deutsche Welle Brasil, assim como o envio desses resultados por e-mail uma vez por dia, com automação da ferramenta Pipedream para o cron-jon.

Todas as bibliotecas necessárias estão em 'requirements.txt' e o site foi desenvolvido via biblioteca 'flask' e em 'python' e 'html' básico. Não foi aplicada a questão de CSS na página dinâmica, mas os templates estão salvos dentro da pasta 'static' dentro deste repositório, assim como as imagens utilizadas.


