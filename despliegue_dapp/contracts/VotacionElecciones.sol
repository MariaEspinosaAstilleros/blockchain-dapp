pragma solidity ^0.5.16;
pragma experimental ABIEncoderV2;

contract VotacionElecciones {

  enum State {Creating, Voting, Ended}

  //Mapeos
  mapping(string => uint) private votes;
  mapping(uint => string) private candidates;
  mapping(address => bool) private vote_emitted;

  //Inicializamos variables
  uint private candidatesCont = 0;
  uint public votesTotal = 0;
  address private owner;
  State private state;

  //Solo el propietario puede modificar la votacion
  modifier modifyOwner() {
    require(msg.sender == owner, "Only owner can modify this ballot");
    _;
  }

  //Una opcion tiene que cambiar de estado
  modifier inState(State _state){
    require(_state == state, "Error");
    _;
  }

  //Se comprueba si se ha votado o no
  modifier ifVoted(address _voter){
    require(!vote_emitted[_voter], "The voter already voted");
    _;
  }

  //Se comprueba si existe el candidato o no
  modifier notExistsCandidate(string memory _candidate){
    bool exists = false;
    for (uint i = 0; i < candidatesCont; i++){
      if (keccak256(bytes(candidates[i])) == keccak256(bytes(_candidate))){
        exists = true;
        break;
      }
    }
    require(exists == false, "The candidate does'nt exists");
    _;
  }

  modifier existsCandidate(string memory _candidate){
    bool exists = false;
    for (uint i = 0; i < candidatesCont; i++){
      if (keccak256(bytes(candidates[i])) == keccak256(bytes(_candidate))){
        exists = true;
        break;
      }
    }
    require(exists == true, "The candidate exists");
    _;
  }

  //Constructor
  constructor(string[] memory _candidates) public {
    owner = msg.sender;
    state = State.Creating;
    for (uint i = 0; i < _candidates.length; i++){
      addCandidate(_candidates[i]);
    }
  }

  //Añadimos un nuevo candidato a la votacion
  function addCandidate(string memory _candidate) public inState(State.Creating) modifyOwner() notExistsCandidate(_candidate){
    votes[_candidate] = 0;
    candidates[candidatesCont] = _candidate;
    candidatesCont++;
  }

  //Iniciamos las votaciones
  function startVoting() public inState(State.Creating) modifyOwner() {
    state = State.Voting;
  }

  //Cerramos votaciones
  function closeVoting() public inState(State.Voting) modifyOwner() {
    state = State.Ended;
  }

  //Emitimos los votos
  function voteFor(string memory _candidate) public inState(State.Voting)
    existsCandidate(_candidate) ifVoted(msg.sender) {
    votesTotal++;
    vote_emitted[msg.sender] = true;
    votes[_candidate]++;
  }

  //Devolvemos a los candidatos
  function showCandidates() public view returns(string[] memory){
    string[] memory retCandidates = new string[](candidatesCont);
    for(uint i = 0; i < candidatesCont; i++){
      retCandidates[i] = candidates[i];
    }
    return retCandidates;
  }

  //Devolvemos al candidato ganador
  function winnerCandidate() public inState(State.Ended) view returns (string memory) {
    string memory actual_winner = "nobody";
    string memory actual_candidate = "nobody";
    uint actual_votes = 0;
    for(uint i = 0; i < candidatesCont; i++){
      actual_candidate = candidates[i];
      if(votes[actual_candidate] > actual_votes){
        actual_winner = actual_candidate;
        actual_votes = votes[actual_candidate];
      }
    }
    return actual_winner;
  }
}

