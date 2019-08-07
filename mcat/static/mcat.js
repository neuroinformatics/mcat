/**
 * mcat.js
 * 
 * @author Takayuki Kannon <kannon@brain.riken.jp>
 */
var flag_drag = false;
var date_table;
var date_table_default = "";

function get_mode() {
	return $("input[type='radio'][name='specify_mode']:checked").val();
}
function set_mode(mode) {
	return $("input[type='radio'][name='specify_mode']").val([ String(mode) ]);
}
function change_mode(obj) {
	var mode = Number(get_mode()) + 1;
	if (mode >= $("input[type='radio'][name='specify_mode']").length)
		mode = 0;
	set_mode(mode);
}
function set_table(obj) {
	set_table_mode(obj,get_mode());
}
function set_table_mode(obj, mode) {
	var row = Number(obj.attr("data-row"));
	var col = Number(obj.attr("data-col"));
	if(date_table[row - 1][col - 1] != '-') {
		if(mode == null || mode == undefined) mode = 1;
		obj.css("background", mode_color[mode]);
		date_table[row - 1][col - 1] = mode;		
	}
}
function fill_table(obj) {
	var row = Number(obj.attr("data-row"));
	var col = Number(obj.attr("data-col"));
	if (row == 0 && col == 0) {
		$("#specify_date_table>tbody>tr>td").each(function() {
			set_table($(this));
		});
	} else if (row == 0) {
		$("#specify_date_table>tbody>tr>td[data-col='" + col + "']").each(
				function() {
					set_table($(this));
				});
	} else if (col == 0) {
		$("#specify_date_table>tbody>tr>td[data-row='" + row + "']").each(
				function() {
					set_table($(this));
				});
	}
}

$(function() {
	var rows = $("#specify_date_table").attr("data-rows");
	var cols = $("#specify_date_table").attr("data-cols");
	date_table = new Array(rows);
	for ( var r = 0; r < rows; r++) {
		date_table[r] = new Array(cols);
		for ( var c = 0; c < cols; c++) {
			set_table_mode($("#specify_date_table>*>tr>td[data-row='" + (r + 1) + "'][data-col='" + (c + 1) + "']"), date_table_default[r * cols + c]);
		}
	}

	$("#specify_date_table>tbody>tr>td")
			.hover(
					function() {
						var row = $(this).attr("data-row");
						var col = $(this).attr("data-col");
						$("#specify_date_table>*>tr>th[data-row='0'][data-col='" + col + "']").css("background", "#ddd");
						$("#specify_date_table>*>tr>th[data-row='" + row + "'][data-col='0']").css("background", "#ddd");
					},
					function() {
						var row = $(this).attr("data-row");
						var col = $(this).attr("data-col");
						$("#specify_date_table>*>tr>th[data-row='0'][data-col='" + col + "']").css("background", "#fff");
						$("#specify_date_table>*>tr>th[data-row='" + row + "'][data-col='0']").css("background", "#fff");
					});
	$("#specify_date_table>tbody>tr>td").mousedown(function() {
		flag_drag = true;
		return false;
	});
	$("#specify_date_table>tbody>tr>td").mousemove(function() {
		if (flag_drag) {
			set_table($(this));
		}
		return false;
	});
	$("#specify_date_table>tbody>tr>td").click(function() {
		set_table($(this));
		return false;
	});
	$("#specify_date_table>tbody>tr>td").dblclick(function() {
		change_mode($(this));
		set_table($(this));
		return false;
	});
	$("#specify_date_table>*>tr>th").mousedown(function() {
		flag_drag = true;
		return false;
	});
	$("#specify_date_table>*>tr>th").mousemove(function() {
		if (flag_drag) {
			fill_table($(this));
		}
		return false;
	});
	$("#specify_date_table>*>tr>th").click(function() {
		fill_table($(this));
		return false;
	});
	$("#specify_date_table>*>tr>th").dblclick(function() {
		change_mode($(this));
		fill_table($(this));
		return false;
	});
	$("body").mouseup(function() {
		flag_drag = false;
		return true;
	});

});