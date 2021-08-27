export default class Game {
    constructor(id, sessionLength, active, wholesalerPresent, retailerPresent, demandPatternId, infoDelay, infoSharing, holdingCost, backlogCost) {
    this.id = id
    this.session_length = sessionLength;
    this.active = active;
    this.wholesaler_present = wholesalerPresent;
    this.retailer_present = retailerPresent;
    this.demand_pattern_id = demandPatternId;
    this.info_delay = infoDelay;
    this.info_sharing = infoSharing;
    this.holding_cost = holdingCost;
    this.backlog_cost = backlogCost;
    }
}