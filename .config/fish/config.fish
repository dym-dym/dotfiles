if status is-interactive
    # Commands to run in interactive sessions can go here
end

function fish_greeting
  #echo (set_color yellow; date +%T; set_color normal) 
end

starship init fish | source

alias antlr4='java -jar /usr/local/lib/antlr-4.9.2-complete.jar'
alias grun='java org.antlr.v4.gui.TestRig'
alias choco='java -classpath /usr/local/lib/choco-solver-4.10.7-jar-with-dependencies.jar'
alias ls='exa -1l --icons'
alias grep='rg'
#alias ranger='joshuto'
#alias ps='procs'
alias tlmgr='/usr/share/texmf-dist/scripts/texlive/tlmgr.pl --usermode'

# [ -f "/home/dymdym/.ghcup/env" ] && source "/home/dymdym/.ghcup/env" # ghcup-env

# export BW_SESSION="6z8JLaphvMi5caEQpy1mYKuZWDZbUtzrXJ/P6eW52w/YGN/lRBpkBip9NejtxPDHBkD7LApTKb1tQ/lA7yhQ4A=="

fish_add_path -p /home/dymdym/.local/bin/ .
set -q GHCUP_INSTALL_BASE_PREFIX[1]; or set GHCUP_INSTALL_BASE_PREFIX $HOME ; set -gx PATH $HOME/.cabal/bin $PATH /home/dymdym/.ghcup/bin # ghcup-env
