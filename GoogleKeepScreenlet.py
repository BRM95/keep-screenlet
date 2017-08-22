#!/usr/bin/env python
import sys
ScreenletPath = sys.path[0]
sys.path.append(ScreenletPath+'/backend/');
import screenlets
import cairo
import pango
import threading
import gtk
import gobject
from screenlets import DefaultMenuItem
from screenlets.options import StringOption, IntOption, ListOption
import keep;
_ = screenlets.utils.get_translator(__file__)

def tdoc(obj):
	obj.__doc__ = _(obj.__doc__)
	return obj

@tdoc
#Then we declare the baseclass itself.


class GoogleKeepScreenlet(screenlets.Screenlet):
    __name__ = 'Keep'
    __version__ = '0.2'
    __author__ = 'Bilal Musani'
    __desc__ = 'A Google Keep screenlet.'
    __content  = [];
    interval = 10;
    __position = [];
    __items = [];
    __selected = None
    __height = 0;
    __width = 250;
    __deleted = [];
    __click = False;
    __text = "";
    pos = [40,40];
    init = False;

    def __init__(self, **kwargs):
        # Customize the width and height.
        screenlets.Screenlet.__init__(self, width=500, height=500,
			uses_theme=True, **kwargs);
        self.update_items();
        self.__height = 320;
        self.__width = (max([len(x) for x in self.__content])-5) *10;
        self.update_contents();
        self.update()

    def on_init(self):
        self.add_default_menuitems();

    def update_contents(self):
        #keep.delete([]);
        self.__timeout = gobject.timeout_add(self.interval * 80000, self.update_contents)

    def update_items(self):
        if self.__deleted:
            self.__deleted = keep.delete(self.__deleted);
        filePath = ScreenletPath + "/files/contents.txt";
        with open(filePath, 'r') as f:
            self.__content = f.read().splitlines();
        self.__deleted = [];
        self.__timeout = gobject.timeout_add(self.interval * 3000, self.update_items)

    def update(self):
        """Update displayed content."""
        self.__items = [];
        for con in self.__content:
            self.__items.append(con)
        if self.__text:
			self.__items.append(self.__text);
        self.__items.append(" ");
        self.redraw_canvas();
        # Set to update again after self.interval.
        self.__timeout = gobject.timeout_add(self.interval * 10, self.update)

    def addNew(self):
        keep.delete(self.__text);
        filePath = ScreenletPath + "/files/contents.txt";
        with open(filePath, 'r') as f:
             self.__content = f.read().splitlines();
        self.__text = "";

    def on_draw(self, ctx):
        """Called every time the screenlet is drawn to the screen."""
        gradient = cairo.LinearGradient(0, self.height * 2, 0, 0)
        gradient.add_color_stop_rgba(0.1, 0.1, 0.1, 0.1, 0.7)
        gradient.add_color_stop_rgba(0.1, 0.1, 0.1, 0.1, 0.75)
        ctx.set_source(gradient)
        self.draw_rectangle_advanced (ctx, self.pos[0], self.pos[1], self.__width - 20,
                                      self.__height - 280,
                                      rounded_angles=(5, 5, 5, 5),
                                      fill=True, border_size=1,
                                      border_color=(0, 0, 0, 0.25),
                                      shadow_size=10,
                                      shadow_color=(0, 0, 0, 0.25))
        # Make sure we have a pango layout initialized and updated.
        if self.p_layout == None :
            self.p_layout = ctx.create_layout()
        else:
            ctx.update_layout(self.p_layout)
        p_fdesc = pango.FontDescription()
        p_fdesc.set_family("Garuda");
        p_fdesc.set_size(20 * pango.SCALE)
        self.p_layout.set_font_description(p_fdesc);
        pos = [(self.pos[0]+self.__width/2-40), self.pos[1]+5]
        ctx.set_source_rgb(1, 1, 1)
        x=0;
        self.__selected = None
        ctx.save()
        ctx.translate(*pos)
        txt = "To-Do";
        self.p_layout.set_markup('%s' % txt)
        ctx.show_layout(self.p_layout)
        ctx.restore()
        x += 1
        p_fdesc.set_family("Free Sans");
        p_fdesc.set_size(10 * pango.SCALE)
        self.p_layout.set_font_description(p_fdesc);
        pos = [self.pos[0]+20, self.pos[1] + 60];
        self.__position = [];
        for item in self.__items:
            ctx.set_source(gradient);
            ctx.set_line_width (10);
            ctx.rectangle(self.pos[0]-20,pos[1]+4,7,7);
            ctx.fill();
            self.__position.append((pos[1]+4,item));
            self.draw_rectangle_advanced (ctx, self.pos[0], pos[1]-14, self.__width - 20,
								  self.__height - (295),
								  rounded_angles=(5, 5, 5, 5),
								  fill=True, border_size=1,
								  border_color=(0, 0, 0, 0.25),
								  shadow_size=10,
								  shadow_color=(0, 0, 0, 0.25))
            ctx.set_source_rgb(0.8,0.8,0.8);
            ctx.save()
            ctx.translate(*pos)
            self.p_layout.set_markup('%s' % item)
            ctx.show_layout(self.p_layout)
            pos[1] += 30
            ctx.restore()
            x += 1

    def on_key_down(self, keycode, keyvalue, event):
        """Called when a keypress-event occured in Screenlet's window."""
        if self.__click == True and (len(gtk.gdk.keyval_name(event.keyval)) < 2 or gtk.gdk.keyval_name(event.keyval) == "space"):
            if gtk.gdk.keyval_name(event.keyval) == "space":
               self.__text = self.__text + " ";
            else:
               self.__text = self.__text + gtk.gdk.keyval_name(event.keyval);
        if gtk.gdk.keyval_name(event.keyval) == "BackSpace" and self.__text:
            self.__text = self.__text[:-1];
        if gtk.gdk.keyval_name(event.keyval) == "Return" or self.__click == False and self.__text:
            self.addNew();
			#screenlets.show_message(self, "Committed");

    def on_draw_shape(self, ctx):
        ctx.rectangle(0, 0, self.width, self.height);
        ctx.fill()

	def on_quit (self):
		"""Callback for handling destroy-event. Perform your cleanup here!"""
        if not self.init:
            return False
        filePath = ScreenletPath + "/files/position.txt";
        thefile = open(filePath, 'w');
        temp = [];
        if self.x<950 or self.x>(self.__width/2+960):
            self.x=self.__width/2+960; self.y=330;
        temp.append(self.x);temp.append(self.y);
        for item in temp:
             thefile.write("%s\n" % item);
        return True

    def on_mouse_down(self, event):
        self.__click = False;
        if self.mousex < (self.pos[0]-10) and self.mousex > (self.pos[0]-25):
           for x,y in self.__position:
               if (x <= self.mousey + 10) and (x >= self.mousey - 10) and y:
                     self.__content = list([i for i in self.__content if i!=y]);
                     self.__position = list([i for i in self.__position if(i[1]!=y)]);
                     if y == self.__text:
                        self.__text = "";
                     self.update();
                     self.__deleted.append(y);
                     break;
        else:
            for x,y in self.__position:
                if (x <= self.mousey + 10) and (x >= self.mousey - 10) and y == " ":
                  self.__click = True;
                  break;

if __name__ == "__main__":
    import screenlets.session
    screenlets.session.create_session(GoogleKeepScreenlet)
