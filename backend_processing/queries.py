tournament ='''
query TournamentsByVideogame($perPage: Int, $startAt : Timestamp) {
  tournaments(query: {
    perPage: $perPage
    page: 0
    sortBy: "startAt asc"
    filter: {
        past : true
        afterDate: $startAt
    } 
  }){
    nodes {
      id
      startAt
      events{
        id
        slug
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
