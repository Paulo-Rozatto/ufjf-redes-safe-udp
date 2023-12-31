# UFJF - Safe UDP

Trabalho referente à disciplina DCC042 Redes de Computadores. O objetivo é construir um protocolo confiaável a partir de um protocolo não confiável UDP.

## Requisitos
1) Entrega ordenada para aplicação baseado na ordem dos pacotes (# de sequência).
2) Confirmação acumulativa (ACK acumulativo) do destinatário para o remetente.
3) Utilização de um Buffer de pacotes de tamanho T, onde pacotes ocupam M Bytes.
4) O tamanho de cada pacote é de, no máximo, 1024 Bytes. (M)
5) Deve haver uma janela deslizante com tamanho N no buffer do remetente e do servidor. Onde N é igual a pelo menos 10 pacotes de tamanho M.
6) Números de sequência devem ser utilizados. Eles podem ser inteiros em um total de N*2, ou serem incrementados conforme o fluxo de bytes, como no TCP.
7) Adicione no protocolo um controle de fluxo, onde o remetente deve saber qual o tamanho da janela N do destinatário, a fim de não afogá-lo.
8) Por fim, crie um equação de controle de congestionamento, a fim de que, se a rede estiver apresentando perda (muitos pacotes com ACK pendentes e timeout), ele deve ser utilizado para reduzir o fluxo de envio de pacotes. Você deve propor um controle de congestionamento, que pode ser baseado em algum do TCP, QUIC ou qualquer outro protocolo. Lembre da Aula 13, onde há controle de congestionamento no TCP que utiliza uma janela "cwnd" e um variável "ssthresh" para controle das fases de "Slow Start" e "Congestiona Avoidance".
9) Avalie seu protocolo sobre 1 remetente (cliente) que envia um arquivo (ou dados sintéticos) de, pelo menos, 10MB, qualquer, para 1 destinatário (servidor). Para avaliar o controle de congestionamento, insira perdas arbitrárias (ou utilizando uma função rand()) de pacotes no destinatário (você pode fazer isso sorteando a cada chegada de um novo pacote se ele será contabilizado e processado ou descartado).