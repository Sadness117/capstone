let itemClick = 0
let curr_move = 0
let curr_game = 0
let curr_item = 0
const first_item = starter_value(`/diff_item/0`)
const first_move = starter_value(`/diff_move/0`)
const first_game = starter_value('/diff_game/0')
let dpad1_id = ''
let dpad3_id = ''


async function starter_value(link){
    //initializes the first of said value so the screen doesnt go blank
    let value = await axios.get(link)
    return value.data
}


async function diff_pokemon(){
    // changes the pokemon on page
    const id = $(this).data('id')
    await axios.get(`/pokemon/${id}`)
    location.reload()
}
async function favorite_pokemon(){
    //adds your favorite pokemon to the database
    const id = $(this).data('id')
    console.log(id)
    added = await axios.post(`/favorite/${id}`)
    alert(added.data)
}

async function next_move() {
    //cycles to the next move in the list
    const id = $(this).data('id')
    curr_move++
    let changed_move = await axios.get(`/diff_move/${curr_move}`)
    if (changed_move.data === 'none'){
        let previous_object = await axios.get(`/diff_move/${curr_move - 1}`)
        curr_move--
        alert('no more moves')
        return previous_object.data
    }
    else{
        let doc = document.getElementById('curr_move')
        return changed_move.data
    }  
}

async function previous_move() {
    //goes back a move in the list
    
    const id = $(this).data('id')
    if (curr_move == 0){
        curr_move = 0
        alert('no previous moves')
        return first_move
    }
    else{
        curr_move--
        let changed_move = await axios.get(`/diff_move/${curr_move}`)
        let doc = document.getElementById('curr_move')
        return changed_move.data
    }
}

async function next_item() {
    //cycles to the next game in the list
    curr_item++
    let changed_item = await axios.get(`/diff_item/${curr_item}`)
    if (changed_item.data === 'none'){
        let previous_object = await axios.get(`/diff_item/${curr_item - 1}`)
        curr_item--
        alert('no more items')
        return previous_object.data
    }
    else{
        let doc = document.getElementById('curr_game')
        return changed_item.data
    }
    
}
async function previous_item() {
    //goes back a move in the list
    
    const id = $(this).data('id')
    if (curr_item == 0){
        curr_item = 0
        alert('no previous item')
        return first_item
    }
    else{
        curr_item--
    
        let changed_item = await axios.get(`/diff_item/${curr_item}`)
        let doc = document.getElementById('curr_move')
        return changed_item.data
    }
}





async function next_game() {
    //cycles to the next game in the list
    const id = $(this).data('id')
    curr_game++
    let changed_game = await axios.get(`/diff_game/${curr_game}`)
    if (changed_game.data === 'none'){
        let previous_object = await axios.get(`/diff_game/${curr_game - 1}`)
        curr_game--
        alert('no more games')
        return previous_object.data
    }
    else{
    let doc = document.getElementById('curr_game')
    return changed_game.data
    }
}
async function previous_game() {
    //cycles to the previous game in the list
    
    const id = $(this).data('id')
    if (curr_game == 0){
        curr_game = 0
        alert('no previous game')
        return first_game
    }
    else{
        curr_game--
        let changed_game = await axios.get(`/diff_game/${curr_game}`)
        let doc = document.getElementById('curr_game')
        return changed_game.data
    }
}

async function remove_fav() {
    //removes favorite pokemon from the database
    const id = $(this).data('id')
    let remove_fav = await axios.post(`/remove_fav/${id}`)
    $("div").remove(`.fav_${id}`);
    console.log(remove_fav)
}

async function display_info(){
    //this will handle what is displayed on the right side
    //of the pokedex, the complicated cases are the 3 if statements
    //below and requires a change in dpads
    //otherwise it will have a simple data selection
    const id = $(this).data('id')
    console.log(id)
    if (id == 'Moves:'){
        console.log('moves')
        dpad_id_change('move_previous', 'move_next')
    }
    else if (id == 'Games:') {
        console.log('game')
        dpad_id_change('game_previous', 'game_next')
    }
    else if (id == 'Items:') {
        dpad_id_change('item_previous', 'item_next')
    }
    
    
    let change_info = await axios.post(`/info/${id}`)
    console.log(change_info.data, id)
    screen_update(change_info.data, id)
}
async function screen_update(content, subject){
    //this will update the screen with called information
    let doc = document.getElementById('info_display')
    let topic = document.getElementById('info_screen')
    doc.textContent = content
    topic.textContent = subject
}
async function test(){
    dpad_id_change('blahh1', 'blahhhh2')
}

async function dpad_id_change(first_change, second_change){
    //this function will change the up and down dpads so the
    //user can scroll through the few lists

    // referenced https://stackoverflow.com/questions/13054286/how-to-set-data-id-attribute/13054354
    // for the setAtribute
    dpad1 = document.getElementById('dpad1')
    dpad1.setAttribute('data-id', first_change)
    dpad1_id = first_change
    dpad3 = document.getElementById('dpad3')
    dpad3.setAttribute('data-id', second_change)
    dpad3_id = second_change
}

async function dpad_control(dpad){
    //this is the up and down dpad hub, it will check the data-id
    //and then will call that specific function to cycle through
    //the selected list
    let id = ''
    const pad = $(this).data('pad')
    if (pad == 'one'){
        id = dpad1_id
    }
    else if (pad == 'three'){
        id = dpad3_id
    }
    
    console.log(id)
    
    if (id == 'game_next'){
        console.log('next_game')
        let info_change = await next_game()
        console.log(info_change)
        screen_update(info_change, 'Games:')
    }
    else if (id =='game_previous'){
        console.log('previous_game')
        let info_change = await previous_game()
        console.log(info_change)
        screen_update(info_change, 'Games:')
    }
    else if (id == 'item_next'){
        console.log('next_item')
        let info_change = await next_item()
        console.log(info_change)
        screen_update(info_change, 'Items:')
    }
    else if (id =='item_previous'){
        console.log('previous_item')
        let info_change = await previous_item()
        console.log(info_change)
        screen_update(info_change, 'Items:')
    }
    else if (id == 'move_next'){
        console.log('next_move')
        let info_change = await next_move()
        console.log(info_change)
        screen_update(info_change, 'Moves:')
    }
    else if (id == 'move_previous'){
        console.log('previous_move')
        let info_change = await previous_move()
        console.log(info_change)
        screen_update(info_change, 'Moves:')
    }
}

$('.favorite_button').click(favorite_pokemon)
$('.remove_fav').click(remove_fav)

//dpads up, right, down, left
$('.dpad1').click(dpad_control)
$('.dpad2').click(diff_pokemon)
$('.dpad3').click(dpad_control)
$('.dpad4').click(diff_pokemon)



//the 8 buttons below screen
$('.type_button').click(display_info)
$('.weight_button').click(display_info)
$('.held_items_button').click(display_info)
$('.moves_button').click(display_info)
$('.games_button').click(display_info)
$('.height_button').click(display_info)
$('.habitat_button').click(display_info)
$('.pokemon_name').click(display_info)


