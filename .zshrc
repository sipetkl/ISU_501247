# if [[ -z "$TMUX" ]]; then
#     wal -i /home/example/Images/wallpapers/purple1.jpg
# fi
clear
fastfetch

# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi
# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:$HOME/.local/bin:/usr/local/bin:$PATH

# Path to your Oh My Zsh installation.
export ZSH="$HOME/.oh-my-zsh"
export XDG_DATA_HOME="$HOME/.local/share"
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_STATE_HOME="$HOME/.local/state"
export XDG_CACHE_HOME="$HOME/.cache"
export PATH="$PATH:/home/example/.local/bin"
export nvim="/home/example/.local/share/bob/nightly/bin/nvim"
export EDITOR="$nvim"

ZSH_THEME="powerlevel10k/powerlevel10k"

plugins=(git)

source $ZSH/oh-my-zsh.sh

export SB_API="http://127.0.0.1:9090"
[ -f "$HOME/.zsecrets" ] && source "$HOME/.zsecrets"

vpn-hy2() {
    curl -s -X PUT "$SB_API/proxies/proxy-select" -H "Authorization: Bearer $SB_SECRET" -H "Content-Type: application/json" -d '{"name":"hy2-out"}' >/dev/null
    notify-send "VPN" "⚡ Hysteria2" -t 2000
}

vpn-naive() {
    curl -s -X PUT "$SB_API/proxies/proxy-select" -H "Authorization: Bearer $SB_SECRET" -H "Content-Type: application/json" -d '{"name":"naive-out"}' >/dev/null
    notify-send "VPN" "🔒 Naive" -t 2000
}

vpn-tor() {
    curl -s -X PUT "$SB_API/proxies/proxy-select" -H "Authorization: Bearer $SB_SECRET" -H "Content-Type: application/json" -d '{"name":"tor-out"}' >/dev/null
    notify-send "VPN" "🧅 Tor" -t 2000
}

vpn-off() {
    curl -s -X PUT "$SB_API/proxies/proxy-select" -H "Authorization: Bearer $SB_SECRET" -H "Content-Type: application/json" -d '{"name":"direct"}' >/dev/null
    notify-send "VPN" "🌐 Direct" -t 2000
}
alias cls='clear && fastfetch'
alias ls='exa -a --tree --level=1 --icons --color=always --group-directories-first'
alias l='exa -la --tree --level=1 --icons --color=always --group-directories-first'
alias n='nvim'
alias cat='bat'
alias py="python3"
alias t="tmux attach || tmux"
#alias hy2-on='hysteria client --config ~/.config/hysteria/client.yaml > /tmp/hysteria.log 2>&1 &'
#alias hy2-off='pkill -f "hysteria client" && echo "hysteria stopped"'
#alias hy2-status='pgrep -f "hysteria client" && echo "running" || echo "stopped"'

# yazi configuration
function y() {
	local tmp="$(mktemp -t "yazi-cwd.XXXXXX")" cwd
	yazi "$@" --cwd-file="$tmp"
	IFS= read -r -d '' cwd < "$tmp"
	[ -n "$cwd" ] && [ "$cwd" != "$PWD" ] && builtin cd -- "$cwd"
	rm -f -- "$tmp"
}

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

