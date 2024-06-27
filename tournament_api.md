```mermaid
	sequenceDiagram
		participant frontend
		participant server

		frontend->>server: POST http://localhost:8080/tournaments/?player_amount=4&name=tournament1
		activate server
		server-->>frontend: {status: 201, tournament_id:1, player_amount: 4, custom_name=null, player_ids:[13, 34, 42], token:efiouvbhlejkenflk34nlkln}
		Note right of server: The server creates a new tournament and the n - 1 players and sends the ids back.
		deactivate server

		Note left of frontend: The following requests have the csrf, session, and tournament tokens in the header
		frontend->>server: PUT/PATCH http://localhost:8080/tournaments/1/players/13/?name=player1&password=1234?custom_name=dude1
		activate server
		server-->>frontend: {status: 201, player_id:13, name:dude1}
		deactivate server

		frontend->>server: PUT/PATCH http://localhost:8080/tournaments/1/players/34/?name=player2&password=1234?
		activate server
		server-->>frontend: {status: 201, player_id:34, name:player2}
		deactivate server

		frontend->>server: PUT/PATCH http://localhost:8080/tournaments/1/players/42/?name=player3&password=1234?custom_name=dude3
		activate server
		server-->>frontend: {status: 201, player_id:42, name:dude3}
		deactivate server

		frontend->>server: GET http://localhost:8080/tournaments/1/
		activate server
		server-->>frontend: {the monster you showed us with the tournament info and the next match | error that it's not complete}
		deactivate server

		frontend->>server: GET http://localhost:8080/tournaments/1/<match_id>
		activate server
		server-->>frontend: {url: "ws://localhost:8080/tournaments/1/<match_id>"}
		deactivate server

```