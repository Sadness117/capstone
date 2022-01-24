let itemClick = 0
let curr_move = 0
let curr_game = 0


async function diff_pokemon(){
    const id = $(this).data('id')
    await axios.get(`/pokemon/${id}`)
    location.reload()
}
async function favorite_pokemon(){
    const id = $(this).data('id')
    added = await axios.post(`/favorite/${id}`)
    console.log(added)
    location.reload()
}
async function items() {
    const id = $(this).data('id')
    itemClick++
    let tests = await axios.get('/test')
    alert(tests.data)
}


async function next_move() {
    const id = $(this).data('id')
    curr_move++
    let changed_move = await axios.post(`/diff_move/${curr_move}`)
    let doc = document.getElementById('curr_move')
    doc.textContent = changed_move.data
    
}

async function previous_move() {
    
    const id = $(this).data('id')
    if (curr_move == 0){
        curr_move = 0
        console.log('no previous moves')
    }
    else{
        curr_move--
        let changed_move = await axios.post(`/diff_move/${curr_move}`)
        let doc = document.getElementById('curr_move')
        doc.textContent = changed_move.data
    }
    
    

}




async function next_game() {
    const id = $(this).data('id')
    curr_game++
    let changed_game = await axios.post(`/diff_game/${curr_game}`)
    let doc = document.getElementById('curr_game')
    doc.textContent = changed_game.data
    
}

async function previous_game() {
    
    const id = $(this).data('id')
    if (curr_game == 0){
        curr_game = 0
        console.log('no previous game')
    }
    else{
        curr_game--
        let changed_game = await axios.post(`/diff_game/${curr_game}`)
        let doc = document.getElementById('curr_game')
        doc.textContent = changed_game.data
    }
    
    

}

async function remove_fav() {
    const id = $(this).data('id')
    let remove_fav = await axios.post(`/remove_fav/${id}`)
    $("div").remove(`.fav_${id}`);
    console.log(remove_fav)
    
}




$('.held_items').click(items)
$('.left_pokedex').click(diff_pokemon)
$('.right_pokedex').click(diff_pokemon)
$('.favorite_button').click(favorite_pokemon)
$('.next_move').click(next_move)
$('.previous_move').click(previous_move)
$('.next_game').click(next_game)
$('.previous_game').click(previous_game)
$('.remove_fav').click(remove_fav)