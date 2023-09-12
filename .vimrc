""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                         Vundle
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set nocompatible
filetype off
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
Plugin 'flazz/vim-colorschemes'
Plugin 'easymotion/vim-easymotion'
Plugin 'scrooloose/nerdtree'
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'
Plugin 'majutsushi/tagbar'
Plugin 'ctrlpvim/ctrlp.vim' " Fuzzy search
Plugin 'tpope/vim-commentary'
Plugin 'ap/vim-css-color'
"Plugin 'Valloric/YouCompleteMe'
"Plugin 'vim-ctrlspace/vim-ctrlspace'
"Plugin 'Shougo/unite.vim'
"Plugin 'vim-syntastic/syntastic'
"Plugin 'airblade/vim-gitgutter'
"Plugin 'Yggdroot/indentLine'

call vundle#end()           
filetype plugin indent on  
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                       EasyMotion
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let g:EasyMotion_do_mapping = 0
let g:EasyMotion_smartcase = 1
"let g:EasyMotion_keys = 'hkyuiopnmwertzxcvbasdgf'
let g:EasyMotion_keys = 'wertasdfg'
nmap <Space> <Plug>(easymotion-overwin-f)
map <Leader>j <Plug>(easymotion-j)
map <Leader>k <Plug>(easymotion-k)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                        File identity
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
augroup project
      autocmd!
        autocmd BufRead,BufNewFile *.h,*.c set filetype=c.doxygen
    augroup END
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                         NerdTree
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"start automatically when vim starts up if no files were specified
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 0 && !exists("s:std_in") | NERDTree | endif
"open automatically when vim starts up on opening a directory
autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 1 && isdirectory(argv()[0]) && !exists("s:std_in") | exe 'NERDTree' argv()[0] | wincmd p | ene | endif
map <C-n> :NERDTreeToggle<CR>
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                         Airline
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let g:airline_theme='violet'
"Automatically displays all buffers when there's only one tab open
let g:airline#extensions#tabline#enabled = 1
let g:airline_powerline_fonts = 1
" let g:airline_section_z=""
let g:airline_enable_fugitive=0
let g:airline_enable_syntastic=0
let g:airline_left_sep=''
let g:airline_right_sep=''
let g:airline_detect_whitespace=0
autocmd VimEnter * AirlineToggleWhitespace
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                    Tagbar (Need ctags)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
nmap <F8> :TagbarToggle<CR>
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"                       CtrlP
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let g:ctrlp_working_path_mode = 'ra'
let g:ctrlp_map = '<c-p>'
let g:ctrlp_cmd = 'CtrlP'
let g:ctrlp_custom_ignore = '\v[\/]\.(|git|bin|tools)$'
let g:ctrlp_user_command = ['.git', 'cd %s && git ls-files -co --exclude-standard']
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
set wildignore+=*/tmp/*,*.so,*.swp,*.zip     " MacOSX/Linux
colorscheme Monokai

set relativenumber
" if has("linux")
"     set gfBM\ Plex\ Mono:h14,:Hack\ 14,Source\ Code\ Pro\ 12,Bitstream\ Vera\ Sans\ Mono\ 11
" elseif has("unix")
"     set gfn=Monospace\ 11
" endif
"
" Disable scrollbars
set guioptions-=r
set guioptions-=R
set guioptions-=l
set guioptions-=L
set tabstop=4
set softtabstop=4
set shiftwidth=4
set noexpandtab
set colorcolumn=80
set t_Co=256
filetype plugin indent on
syntax on
set autoread
set encoding=utf-8
set scrolloff=10
set sidescrolloff=5
" Stop word wrapping
set nowrap
  " Except... on Markdown. That's good stuff.
  autocmd FileType markdown setlocal wrap
set showcmd
set laststatus=2
set hidden
" No special per file vim override configs
set nomodeline
" Use system clipboard
set clipboard=unnamedplus
" Don't let Vim hide characters or make loud dings
set conceallevel=1
set noerrorbells
" Use search highlighting
set hlsearch " :noh to cancel highlighting
" Disable mouse support
set mouse=r
let $NVIM_TUI_ENABLE_CURSOR_SHAPE=1

nnoremap <Tab> :bnext!<CR>
nnoremap <S-Tab> :bprev!<CR><Paste>

" The cursor should stay where you leave it, instead of moving to the first non
" blank of the line
"set nostartofline
" Disable wrapping long string
"set nowrap

" Display Line numbers
"set number

" Highlight line with cursor
set cursorline

set textwidth=80

"set &path.="src/include,/usr/include/AL,"
