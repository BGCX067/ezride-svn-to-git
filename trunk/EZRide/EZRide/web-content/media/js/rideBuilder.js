function loadSVG(graph_id, subgraph_id) {
	$('#graph').svg();
	$('#graph').load('/graphs/' + graph_id + '/render/' + subgraph_id + '/');	
}

function graphHover(svg) {
	svg.style('.hovered {fill: red;}');
	$($('#graph'), svg.root()).hover(function() {	
		$(this).addClass('hovered');
	}, function() {		
		$(this).removeClass('hovered');		
	});
}