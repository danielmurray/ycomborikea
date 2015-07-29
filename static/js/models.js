// Models
StartupOrFurniture = Backbone.Model.extend({
  url: '/ycomborikea',
  defaults: {
    'id': 0,
    'name': '',
    'url': '',
    'desc': '',
    'ikea_name': '',
    'ycomb_name': '',
    'product': '',
    'startup': '',
    'cycle': '',
    'product_vote': 0,
    'startup_vote': 0,
  },
  
  addVote: function(vote){
    if( vote == "ikea" ){
      this.save('product_vote', this.get('product_vote') + 1);
    }else{
      this.save('startup_vote', this.get('startup_vote') + 1);
    }
  }

});