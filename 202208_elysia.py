import tkinter as tk

class main:
    class Btn(tk.Button):
        def __init__(self, master, xy, **kw):
            tk.Button.__init__(self, master, **kw)
            self.xy = xy
            self._state = 0
            self._num = 0

    def __init__(self, width=12, height=6):
        self.width = width
        self.height = height
        self._num = 0

    def run(self):
        self._tk = tk.Tk()
        self._tk.title('Elysia')

        self._line = tk.Label(self._tk, text='放置了 0 个妖精爱莉')
        self._line.grid(row=0, column=0, columnspan=3)

        self._dict = {}

        for y in range(self.height):
            for x in range(self.width):
                self._dict[(x, y)] = self.Btn(self._tk, xy=(x, y),
                                          width=4, height=2, bd=1, relief='ridge')
                self._dict[(x, y)].bind('<ButtonRelease-1>',
                                    lambda event: self.click(event.widget))
                self._dict[(x, y)].grid(row=y+1, column=x, sticky='nswe')
                self._dict[(x, y)].configure(
                    bg='green', text=0, font=('黑体', 20, 'bold'))
                # (,relief='flat')

        self._tk.mainloop()

    def click(self, widget):
        x, y = widget.xy
        _add = 0

        if widget._state:
            widget._state = 0
            widget.configure(bg='green')
            _add = -1
        else:
            widget.configure(bg='pink')
            widget._state = 1
            _add = 1

        self._num += _add
        self._line['text'] = '放置了 %d 个妖精爱莉' % self._num

        atk = [
            (x+1, y+1),
            (x+2, y+1),
            (x+3, y+1),
            (x+4, y+1),
            (x+4, y+2),
            (x+5, y+2),
            (x+6, y+2),
            (x+6, y+3),
            (x+7, y+3),
            (x+8, y+3),

            (x+1, y-1),
            (x+2, y-1),
            (x+3, y-1),
            (x+4, y-1),
            (x+4, y-2),
            (x+5, y-2),
            (x+6, y-2),
            (x+6, y-3),
            (x+7, y-3),
            (x+8, y-3),

            (x+1, y),
            (x+2, y),
            (x+3, y),
            (x+4, y),
            (x+5, y),
            (x+6, y),
            (x+7, y),
            (x+8, y),
            (x+9, y),
            (x+10, y),
            (x+11, y),
            (x+12, y),
            (x+13, y),
            (x+14, y),
            (x+15, y),
        ]

        for xx, yy in atk:
            if 0 <= xx <= self.width - 1 and 0 <= yy <= self.height - 1:
                self._dict[(xx, yy)]._num += _add
                self._dict[(xx, yy)].configure(text=self._dict[(xx, yy)]._num)

main(12, 5).run()
