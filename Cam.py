import customtkinter as _9_, tkinter.scrolledtext as _3_, socket as _6_, threading as _5_, queue as _2_
from tkinter import messagebox as _7_, simpledialog as _8_, PhotoImage as _1_
import cv2 as _4_, PIL.Image as _0_, PIL.ImageTk as _b_
import multiprocessing as _d_

_q_ = _2_.Queue()
_s_ = _5_.Event()

_9_.set_appearance_mode("dark")
_9_.set_default_color_theme("dark-blue")


def _c_(_x_, _y_, _z_):
    def _f_():
        try:
            if _y_ and _z_:
                _w_ = f"rtsp://{_y_}:{_z_}@{_x_}/stream"
            else:
                _w_ = f"rtsp://{_x_}/stream"
            _t_ = _4_.VideoCapture(_w_)
            if not _t_.isOpened():
                raise ValueError("Cannot open stream.")

            def _u_():
                if not _s_.is_set():
                    _v_, _a_ = _t_.read()
                    if _v_:
                        _a_ = _4_.cvtColor(_a_, _4_.COLOR_BGR2RGB)
                        _p_ = _0_.fromarray(_a_)
                        _g_ = _b_.PhotoImage(image=_p_)
                        _q_.put(_g_)
                    _m_.after(10, _u_)

            _l_ = _9_.CTkToplevel(_n_)
            _l_.title("IP Camera Stream by | TheZ |")
            _l_.geometry("800x600")

            global _m_
            _m_ = _9_.CTkLabel(_l_)
            _m_.pack()

            _u_()
        except Exception as _j_:
            _7_.showerror("Error", str(_j_))

    _5_.Thread(target=_f_, daemon=True).start()


def _e_():
    global _h_, _k_, _r_
    _i_ = _h_.get()
    _j_ = _k_.get()
    _l_ = _r_.get()
    if not _i_:
        _7_.showerror("Error", "Need IP Address!")
        return
    _c_(_i_, _j_, _l_)


def _x_(_y_):
    _z_ = _y_.split('.')
    _z_[3] = '254'
    return '.'.join(_z_)


def _aa_(_ab_, __ac__, _ad_):
    _ae_ = _x_(_ab_)
    _af_ = list(map(int, _ab_.split('.')))
    _ag_ = list(map(int, _ae_.split('.')))

    def _ah_(_ai_):
        _ai_[3] += 1
        for _aj_ in (3, 2, 1):
            if _ai_[_aj_] == 256:
                _ai_[_aj_] = 0
                _ai_[_aj_ - 1] += 1
        return _ai_

    def _ak_(_al_):
        try:
            _am_ = _6_.socket(_6_.AF_INET, _6_.SOCK_STREAM)
            _am_.settimeout(1)
            _an_ = _am_.connect_ex((_al_, __ac__))
            if _an_ == 0:
                _ad_.put(_al_)
            _am_.close()
        except Exception as _ao_:
            _ad_.put(f"Error scanning {_al_}: {_ao_}")

    _ap_ = _af_
    _aq_ = []
    while _ap_ <= _ag_:
        if _s_.is_set():
            break
        _ar_ = ".".join(map(str, _ap_))
        _as_ = _5_.Thread(target=_ak_, args=(_ar_,))
        _as_.start()
        _aq_.append(_as_)
        _ap_ = _ah_(_ap_)

    for _at_ in _aq_:
        _at_.join()


def _au_():
    return "192.168.1.0"


def _av_():
    return "100.100.100.0"


def _aw_(mode='custom'):
    _ax_ = None
    if mode == 'home':
        _ax_ = _au_()
    elif mode == 'nearby':
        _ax_ = _av_()
    else:
        _ax_ = _h1_.get()

    if not _ax_:
        _7_.showerror("Error", "Need Start IP Address!")
        return

    _ay_ = _x_(_ax_)
    _az_.delete(1.0, _9_.END)
    _az_.insert(_9_.END, f"Scanning: {_ax_} - {_ay_}\n")

    __ac__ = 554
    _ad_ = _2_.Queue()

    def _ba_():
        try:
            _aa_(_ax_, __ac__, _ad_)
            _q_.put("done")
        except Exception as _bb_:
            _q_.put(f"Error: {_bb_}")

    _5_.Thread(target=_ba_, daemon=True).start()

    def _bc_():
        try:
            _bd_ = _q_.get_nowait()
            if _bd_ == "done":
                _az_.insert(_9_.END, "Scan complete.\n")
            elif "Error" in _bd_:
                _7_.showerror("Error", _bd_)
            else:
                _az_.insert(_9_.END, f"Found Camera: {_bd_}\n")
        except _2_.Empty:
            pass
        _az_.after(100, _bc_)

    _bc_()


def _be_():
    _s_.set()
    _az_.insert(_9_.END, "Scanning stopped by user.\n")


def _info_():
    _bf_ = (
        "IP Camera Scanner by TheZ\n\n"
        "Instructions:\n"
        "1. Enter an IP address in the 'Camera Start IP' field to scan.\n"
        "2. Optionally provide a username and password for secure streams.\n"
        "3. Press 'Start Stream' to begin viewing the camera stream.\n"
        "4. Use 'Scan Home Network' to scan your local network.\n"
        "5. Use 'Scan Nearby' to enter a kilometer radius for nearby IP scans.\n"
        "6. You can stop scanning anytime by pressing 'Stop Scan'."
    )
    _7_.showinfo("Help & Instructions", _bf_)


def _scan_nearby_radius_():
    _radius_ = _8_.askinteger("Enter Radius", "Enter the kilometer radius for nearby IP scan:")
    if _radius_:
        _aw_("nearby")


_n_ = _9_.CTk()
_n_.title("IP Camera Scanner by | TheZ |")
_n_.geometry("500x650")
_n_.configure(fg_color="#222")

_n_.wm_iconbitmap("icon.ico")

_h0_ = _9_.CTkLabel(_n_, text="IP Camera Scanner by TheZ", font=("Arial", 18, "bold"), fg_color="#111")
_h0_.pack(pady=10)

_h1_ = _9_.CTkLabel(_n_, text="Camera Start IP", font=("Arial", 12), fg_color="#111", text_color="red")
_h1_.pack(pady=5)
_h2_ = _9_.CTkEntry(_n_, font=("Arial", 12), width=300)
_h2_.pack()

_h3_ = _9_.CTkLabel(_n_, text="Username (Optional)", font=("Arial", 12), fg_color="#111", text_color="blue")
_h3_.pack(pady=5)
_k_ = _9_.CTkEntry(_n_, font=("Arial", 12), width=300)
_k_.pack()

_h4_ = _9_.CTkLabel(_n_, text="Password (Optional)", font=("Arial", 12), fg_color="#111", text_color="blue")
_h4_.pack(pady=5)
_r_ = _9_.CTkEntry(_n_, font=("Arial", 12), width=300, show="*")
_r_.pack()

_h5_ = _9_.CTkButton(_n_, text="Start Stream", command=_e_, fg_color="red", hover_color="gray")
_h5_.pack(pady=10)

_h6_ = _9_.CTkLabel(_n_, text="IP Camera Scanner", font=("Arial", 14, "bold"), fg_color="#111", text_color="white")
_h6_.pack(pady=10)

_h7_ = _9_.CTkButton(_n_, text="Scan Custom", command=lambda: _aw_('custom'), fg_color="red", hover_color="gray")
_h7_.pack(pady=10)

_h8_ = _9_.CTkButton(_n_, text="Scan Home Network", command=lambda: _aw_('home'), fg_color="red", hover_color="gray")
_h8_.pack(pady=10)

_h9_ = _9_.CTkButton(_n_, text="Scan Nearby (Radius)", command=_scan_nearby_radius_, fg_color="red", hover_color="gray")
_h9_.pack(pady=10)

_i0_ = _9_.CTkButton(_n_, text="Stop Scan", command=_be_, fg_color="red", hover_color="gray")
_i0_.pack(pady=10)

_az_ = _3_.ScrolledText(_n_, font=("Arial", 12), width=50, height=10, bg="#222", fg="white")
_az_.pack(pady=10)

_info_button_ = _9_.CTkButton(_n_, text="?", command=_info_, width=40, height=40, fg_color="gray", hover_color="red", font=("Arial", 20))
_info_button_.place(relx=0.95, rely=0.05, anchor="ne")

_n_.mainloop()
