export default class GameState {
    constructor(inventory, week, holding_cost, backlog_cost, incoming_orders, outgoing_orders) {
        this.inventory = inventory;
        this.week = week;
        this.holding_cost = holding_cost;
        this.backlog_cost = backlog_cost;
        this.incoming_orders = incoming_orders;
        this.outgoing_orders = outgoing_orders;
    }
}