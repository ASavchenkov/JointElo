
tournament ='''
query TournamentsByVideogame($perPage: Int, $page : Int) {
  tournaments(query: {
    perPage: $perPage
    page: $page
    sortBy: "startAt asc"
    filter: {
      past: true
      videogameIds: [
        1386
      ]
    }
  }) {
    nodes {
      id
      events{
        id
        name
        videogame {
          id
        }
      }
    }
  }
}
'''

event = '''
query Event($id: Int) {
  
  	
    event(id: $id){
        name
        phaseGroups {
          id
        }
    }
}

'''

phase_group = '''

query PhaseGroup($id: Int) {
  
  	
  phaseGroup( id : $id){
    sets {
      id
      games {
        id
        selections {
          selectionType
          selectionValue
        }
        
      }
    }
  }
}
'''
