return {
  "williamboman/mason.nvim",
  dependencies = {
    "williamboman/mason-lspconfig.nvim",
    "WhoIsSethDaniel/mason-tool-installer.nvim",
    "mfussenegger/nvim-dap",
    "jay-babu/mason-nvim-dap.nvim",
  },

  config = function()
    -- import mason
    local mason = require("mason")

    -- import mason-lspconfig
    local mason_lspconfig = require("mason-lspconfig")
    local mason_tool_installer = require("mason-tool-installer")
    local mason_dap = require("mason-nvim-dap")

    -- enable mason and configure icons
    mason.setup({
      ui = {
        icons = {
          package_installed = "✓",
          package_pending = "➜",
          package_uninstalled = "✗",
        },
      },
    })

    mason_lspconfig.setup({
      -- Language servers
      ensure_installed = {
        -- "tsserver",
        "html",
        "cssls",
        "tailwindcss",
        "svelte",
        "lua_ls",
        "graphql",
        "emmet_ls",
        "prismals",
        "pyright",
        "clangd",
        "vimls",
        "jsonls",
        "lemminx",
        "yamlls",
        "somesass_ls",
        -- "r_language_server",
        "ltex",
        "autotools_ls",
        "marksman",
        "dockerls",
        "docker_compose_language_service",
        "cmake",
        -- "csharp_ls",
        "bashls",
        "arduino_language_server",
        "angularls",
      },
      -- auto-install configured servers (with lspconfig)
      automatic_installation = true, -- not the same as ensure_installed
    })

    mason_tool_installer.setup({
      ensure_installed = {

        -- Formatter and Linters
        "cmakelang", -- CMake
        "markdownlint", --Markdown

        -- Linters
        "pylint", -- Python
        "eslint_d", -- Javascript and more
        "cmakelint", -- CMake
        "luacheck", -- Lua
        "jsonlint", -- Json
        "golangci-lint", -- Golang
        "checkstyle", -- Overall
        "yamllint", -- Yaml
        "stylelint", -- CSS/SCSS etc

        -- Formatters
        "stylua", -- lua
        "prettier",
        "isort", -- python
        "black", -- python
        "htmlbeautifier", -- HTML
        "beautysh", --Shell
        "latexindent", --Latex
        -- "csharpier", --C#
        "clang-format", --C/C++
        "pretty-php", --PHP

        -- Debugger adapters
        "bash-debug-adapter", -- Shell
        "codelldb", -- C/C++/Rust
        "debugpy", -- Python
        "java-debug-adapter", -- Java
        "js-debug-adapter", -- Javascript
        "kotlin-debug-adapter", -- Kotlin
        "netcoredbg", -- C#
        "php-debug-adapter", -- PHP
      },
    })

    local lint_augroup = vim.api.nvim_create_augroup("lint", { clear = true })
  end,
}
