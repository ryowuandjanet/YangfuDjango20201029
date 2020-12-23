// 不可下載最新版本，要下載1.2.1版
(function (a) {
  a.fn.formset = function (c) {
    var l = a.extend({}, a.fn.formset.defaults, c),
      i = l.extraClasses.join(" "),
      j = a(this),
      b = function (n, m) {
        if (l.extraClasses) {
          n.removeClass(i);
          n.addClass(l.extraClasses[m % l.extraClasses.length]);
        }
      },
      k = function (p, q, n) {
        var m = new RegExp("(" + q + "-\\d+-)|(^)"),
          o = q + "-" + n + "-";
        if (p.attr("for")) {
          p.attr("for", p.attr("for").replace(m, o));
        }
        if (p.attr("id")) {
          p.attr("id", p.attr("id").replace(m, o));
        }
        if (p.attr("name")) {
          p.attr("name", p.attr("name").replace(m, o));
        }
      },
      e = function (m) {
        return m.find("input,select,textarea,label").length > 0;
      },
      f = function (m) {
        if (m.is("TR")) {
          m.children(":last").append('<a class="' + l.deleteCssClass + '" href="javascript:void(0)">' + l.deleteText + "</a>");
        } else {
          if (m.is("UL") || m.is("OL")) {
            m.append('<li><a class="' + l.deleteCssClass + '" href="javascript:void(0)">' + l.deleteText + "</a></li>");
          } else {
            m.append('<a class="' + l.deleteCssClass + '" href="javascript:void(0)">' + l.deleteText + "</a>");
          }
        }
        m.find("a." + l.deleteCssClass).click(function () {
          var r = a(this).parents("." + l.formCssClass),
            n = r.find('input:hidden[id $= "-DELETE"]');
          if (n.length) {
            n.val("on");
            r.hide();
          } else {
            r.remove();
            var o = a("." + l.formCssClass).not(".formset-custom-template");
            a("#id_" + l.prefix + "-TOTAL_FORMS").val(o.length);
            for (var p = 0, q = o.length; p < q; p++) {
              b(o.eq(p), p);
              o.eq(p)
                .find("input,select,textarea,label")
                .each(function () {
                  k(a(this), l.prefix, p);
                });
            }
          }
          if (l.removed) {
            l.removed(r);
          }
          return false;
        });
      };
    j.each(function (n) {
      var o = a(this),
        m = o.find('input:checkbox[id $= "-DELETE"]');
      if (m.length) {
        m.before('<input type="hidden" name="' + m.attr("name") + '" id="' + m.attr("id") + '" />');
        m.remove();
      }
      if (e(o)) {
        f(o);
        o.addClass(l.formCssClass);
        b(o, n);
      }
    });
    if (j.length) {
      var g, h;
      if (l.formTemplate) {
        h = l.formTemplate instanceof a ? l.formTemplate : a(l.formTemplate);
        h.removeAttr("id").addClass(l.formCssClass).addClass("formset-custom-template");
        h.find("input,select,textarea,label").each(function () {
          k(a(this), l.prefix, 2012);
        });
        f(h);
      } else {
        h = a("." + l.formCssClass + ":last")
          .clone(true)
          .removeAttr("id");
        h.find('input:hidden[id $= "-DELETE"]').remove();
        h.find("input,select,textarea,label").each(function () {
          var m = a(this);
          if (m.is("input:checkbox") || m.is("input:radio")) {
            m.attr("checked", false);
          } else {
            m.val("");
          }
        });
      }
      l.formTemplate = h;
      if (j.attr("tagName") == "TR") {
        var d = j.eq(0).children().length;
        j.parent().append('<tr><td colspan="' + d + '"><a class="' + l.addCssClass + '" href="javascript:void(0)">' + l.addText + "</a></tr>");
        g = j.parent().find("tr:last a");
        g.parents("tr").addClass(l.formCssClass + "-add");
      } else {
        j.filter(":last").after('<a class="' + l.addCssClass + '" href="javascript:void(0)">' + l.addText + "</a>");
        g = j.filter(":last").next();
      }
      g.click(function () {
        var n = parseInt(a("#id_" + l.prefix + "-TOTAL_FORMS").val()),
          o = l.formTemplate.clone(true).removeClass("formset-custom-template"),
          m =
            a(this)
              .parents("tr." + l.formCssClass + "-add")
              .get(0) || this;
        b(o, n);
        o.insertBefore(a(m)).show();
        o.find("input,select,textarea,label").each(function () {
          k(a(this), l.prefix, n);
        });
        a("#id_" + l.prefix + "-TOTAL_FORMS").val(n + 1);
        if (l.added) {
          l.added(o);
        }
        return false;
      });
    }
    return j;
  };
  a.fn.formset.defaults = {
    prefix: "form",
    formTemplate: null,
    addText: "add another",
    deleteText: "remove",
    addCssClass: "add-row",
    deleteCssClass: "delete-row",
    formCssClass: "dynamic-form",
    extraClasses: [],
    added: null,
    removed: null,
  };
})(jQuery);
