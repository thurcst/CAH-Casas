[[User Flow.excalidraw]]
## Lobby
#Documentação 

![[Pasted image 20240430231239.png]]
> [[Lobby]]

1. Jogador entra na página inicial da aplicação
2. Escolhe seu nome e decide entre criar e entrar em uma sala
3. Caso ele decida por criar:
	1. Ele recebe as informações da sala e é redirecionado para tela de Lobby
	2. Pode alterar informações da sala
	3. Pode iniciar o jogo
4. Caso ele decida entrar:
	1. Deve aguardar o dono da sala iniciar o jogo
5. Ao jogo ser iniciado todos serão redirecionados para tela de jogo

## Ingame

![[Pasted image 20240430231212.png]]
> [[Iniciar jogo]]

1. Jogo é iniciado
2. O jogo distribui 10 cartas de resposta para todos os jogadores
3. A primeira pergunta é distribuída automaticamente pelo jogo
4. Cada jogador escolhe uma carta branca
5. A rodada finaliza e é iniciada a votação
6. O vencedor da votação recebe `+1` ponto e é responsável por decidir a carta de pergunta para a próxima rodada
7. As etapas 4 a 6 são repetidas até o limite de pontuação ou limite de rodadas chegarem
8. A tela de vencedor é apresentada
9. Jogadores são redirecionados para a tela de `Lobby`
