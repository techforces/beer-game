const api_url = 'http://localhost:8086'
 mocha.setup('bdd');
describe('test', () => {
    let randnum = (Math.floor(Math.random() * 10203040))
    auth_name = 'user_test'+ randnum
    auth_pass = '12345'
    function getfromserver(url, data, headers=null){
        return $.ajax({
            url: url,
            headers: headers,
            type:  'POST',
            data: JSON.stringify(data),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json'
        });
    }
    it('test player registration', async () => {
        let x = await getfromserver(api_url + '/register',{
            email: auth_name,
            passwordHash: auth_pass,
            role: "player"
        })
        chai.expect(x['SESSION-KEY']).not.equal(null)
    });

    it('registered player can authenticate multiple times', async()=>{
        let x = await getfromserver(api_url + '/authenticate', {
            email: auth_name,
            passwordHash: auth_pass
        })
        chai.expect(x['SESSION-KEY']).not.equal(null)
    })
    let randnum2 = (Math.floor(Math.random() * 10203040))
    auth_name2 = 'player_test'+ randnum2
    auth_pass2 = '12345'

    it('test instructor registration', async() =>{
        let x = await getfromserver(api_url + '/register',{
            email: auth_name2,
            passwordHash: auth_pass2,
            role: "instructor"
        })
        chai.expect(x['SESSION-KEY']).not.equal(null)
    })

    it('registered instructor can authenticate multiple times', async()=>{
        let x = await getfromserver(api_url + '/authenticate', {
            email: auth_name2,
            passwordHash: auth_pass2
        })
        chai.expect(x['SESSION-KEY']).not.equal(null)
    })

    it('instructor can create game', async()=>{
        // try to be atomic in our testing
        let x = await getfromserver(api_url + '/authenticate', {
            email: auth_name2,
            passwordHash: auth_pass2
        })
        chai.expect(x['SESSION-KEY']).not.equal(null)
        console.log(x)
        let game_creation = await getfromserver(api_url + '/instructor/game', {
        }, {'SESSION-KEY': x['SESSION-KEY']})
        console.log(game_creation)
        chai.expect(game_creation['game_id']).not.equal(null)
    })

    it('non-authenticated user cannot create game', async()=>{
        // this should surely fail since we do not include the header
        try{
            let game_creation = await getfromserver(api_url + '/instructor/game', {
            })
            console.log(game_creation)
            chai.expect(1).to.eql(2).withErrorMessage("expected an error to be thrown");
        }
        catch(err){
            return
        } 
    })
    let params = {
        "session_length": 21,
        "retailer_present": true,
        "wholesaler_present": false,
        "holding_cost": 6.9,
        "backlog_cost": 4.20,
        "active": true,
        "starting_inventory": 5,
        "info_delay": 22,
        "info_sharing": true,
    }
    it('instructor can create game with custom parameters', async()=>{
        // try to be atomic in our testing
        let x = await getfromserver(api_url + '/authenticate', {
            email: auth_name2,
            passwordHash: auth_pass2
        })
        chai.expect(x['SESSION-KEY']).not.equal(null)
        console.log(x)

        let game_creation = await getfromserver(api_url + '/instructor/game', params, {'SESSION-KEY': x['SESSION-KEY']})
        console.log(game_creation)
        chai.expect(game_creation['game_id']).not.equal(null)
        //now get all the game parameters
    })
    it('can get game info, game info is correct', async()=>{
        // try to be atomic in our testing
        let x = await getfromserver(api_url + '/authenticate', {
            email: auth_name2,
            passwordHash: auth_pass2
        })
        chai.expect(x['SESSION-KEY']).not.equal(null)
        // create another game just to be sure
        let game_creation = await getfromserver(api_url + '/instructor/game', params, {'SESSION-KEY': x['SESSION-KEY']})
        console.log(game_creation)
        chai.expect(game_creation['game_id']).not.equal(null)
        r = await $.ajax({
            url: api_url+'/instructor/game/'+game_creation['game_id'],
            headers: {'SESSION-KEY': x['SESSION-KEY']},
            type:  'GET',
            contentType: 'application/json; charset=utf-8',
            dataType: 'json'
        });
        for (var k in params){
            // EXPLICITLY USE == BECAUSE OF TYPE MISMATCHES
            chai.assert(params[k] == r[k])
            console.log(`comparing: (${params[k]}, ${r[k]})`)
        }
               //now get all the game parameters
    }) 
});