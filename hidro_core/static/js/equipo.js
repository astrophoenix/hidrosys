var equipo = {

	init : function()
	{
		btn_buscar_mediciones.click(buscar_mediciones);
		setInterval( "actualizar()", 10000);
	},

	actualizar : function(url)
	{
		$('#contenido_mediciones').fadeOut("slow").load('url #tabla_mediciones').fadeIn("slow");
	},
	

};

$(function(){
	equipo.init();
});