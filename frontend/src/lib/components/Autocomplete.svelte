<script lang="ts">
    import { fly } from "svelte/transition";
    import { Loader2 } from "lucide-svelte";

    // Props
    let {
        value = $bindable(""),
        placeholder = "Search...",
        searchFn,
        onSelect,
        disabled = false,
    }: {
        value?: string;
        placeholder?: string;
        searchFn: (
            query: string,
        ) => Promise<Array<{ value: string; label: string }>>;
        onSelect?: (item: { value: string; label: string }) => void;
        disabled?: boolean;
    } = $props();

    // State
    let inputValue = $state(value);
    let results = $state<Array<{ value: string; label: string }>>([]);
    let isOpen = $state(false);
    let isLoading = $state(false);
    let selectedIndex = $state(-1);
    let debounceTimer: ReturnType<typeof setTimeout>;
    let inputRef: HTMLInputElement;

    // Sync external value changes
    $effect(() => {
        if (value !== inputValue) {
            inputValue = value;
        }
    });

    const search = async (query: string) => {
        if (query.length < 1) {
            results = [];
            isOpen = false;
            return;
        }

        isLoading = true;
        try {
            results = await searchFn(query);
            isOpen = results.length > 0;
            selectedIndex = -1;
        } catch (e) {
            console.error("Autocomplete search failed:", e);
            results = [];
        } finally {
            isLoading = false;
        }
    };

    const handleInput = (e: Event) => {
        const target = e.target as HTMLInputElement;
        inputValue = target.value;
        value = target.value;

        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => search(inputValue), 300);
    };

    const selectItem = (item: { value: string; label: string }) => {
        inputValue = item.label;
        value = item.value;
        isOpen = false;
        results = [];
        onSelect?.(item);
    };

    const handleKeydown = (e: KeyboardEvent) => {
        if (!isOpen) return;

        switch (e.key) {
            case "ArrowDown":
                e.preventDefault();
                selectedIndex = Math.min(selectedIndex + 1, results.length - 1);
                break;
            case "ArrowUp":
                e.preventDefault();
                selectedIndex = Math.max(selectedIndex - 1, -1);
                break;
            case "Enter":
                e.preventDefault();
                if (selectedIndex >= 0 && results[selectedIndex]) {
                    selectItem(results[selectedIndex]);
                }
                break;
            case "Escape":
                isOpen = false;
                selectedIndex = -1;
                break;
        }
    };

    const handleBlur = () => {
        // Delay to allow click events on dropdown items
        setTimeout(() => {
            isOpen = false;
        }, 200);
    };
</script>

<div class="autocomplete-wrapper">
    <div class="input-container">
        <input
            bind:this={inputRef}
            type="text"
            {placeholder}
            {disabled}
            value={inputValue}
            oninput={handleInput}
            onkeydown={handleKeydown}
            onfocus={() =>
                inputValue.length >= 1 && results.length > 0 && (isOpen = true)}
            onblur={handleBlur}
            class:loading={isLoading}
        />
        {#if isLoading}
            <div class="loading-indicator">
                <Loader2 size={14} class="spin" />
            </div>
        {/if}
    </div>

    {#if isOpen && results.length > 0}
        <div class="dropdown" transition:fly={{ y: -5, duration: 150 }}>
            {#each results as item, index}
                <button
                    type="button"
                    class="dropdown-item"
                    class:selected={index === selectedIndex}
                    class:city-item={item.type === "city"}
                    onclick={() => selectItem(item)}
                    onmouseenter={() => (selectedIndex = index)}
                >
                    {#if item.type === "city"}
                        <span class="city-icon">🌐</span>
                    {/if}
                    <span class="item-label">{item.label}</span>
                </button>
            {/each}
        </div>
    {/if}
</div>

<style>
    .autocomplete-wrapper {
        position: relative;
        width: 100%;
    }

    .input-container {
        position: relative;
    }

    input {
        width: 100%;
        padding: 0.5rem 0.75rem;
        background: rgba(0, 30, 15, 0.6);
        border: 1px solid rgba(0, 230, 118, 0.3);
        border-radius: 6px;
        color: #fff;
        font-size: 0.9rem;
        outline: none;
        transition:
            border-color 0.2s,
            box-shadow 0.2s;
        box-sizing: border-box;
    }

    input:focus {
        border-color: rgba(0, 230, 118, 0.6);
        box-shadow: 0 0 0 2px rgba(0, 230, 118, 0.1);
    }

    input::placeholder {
        color: rgba(255, 255, 255, 0.4);
    }

    input.loading {
        padding-right: 2rem;
    }

    .loading-indicator {
        position: absolute;
        right: 0.5rem;
        top: 50%;
        transform: translateY(-50%);
        color: #00e676;
    }

    :global(.loading-indicator .spin) {
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    .dropdown {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        margin-top: 4px;
        background: rgba(10, 20, 15, 0.98);
        border: 1px solid rgba(0, 230, 118, 0.3);
        border-radius: 6px;
        max-height: 240px;
        overflow-y: auto;
        z-index: 100;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    }

    .dropdown-item {
        display: block;
        width: 100%;
        padding: 0.6rem 0.75rem;
        background: transparent;
        border: none;
        color: #fff;
        font-size: 0.85rem;
        text-align: left;
        cursor: pointer;
        transition: background 0.15s;
    }

    .dropdown-item:hover,
    .dropdown-item.selected {
        background: rgba(0, 230, 118, 0.15);
    }

    .dropdown-item:first-child {
        border-radius: 5px 5px 0 0;
    }

    .dropdown-item:last-child {
        border-radius: 0 0 5px 5px;
    }

    /* City group options */
    .dropdown-item.city-item {
        background: rgba(0, 230, 118, 0.08);
        font-weight: 600;
        border-left: 3px solid #00e676;
    }

    .dropdown-item.city-item:hover,
    .dropdown-item.city-item.selected {
        background: rgba(0, 230, 118, 0.2);
    }

    .city-icon {
        margin-right: 0.5rem;
    }

    .item-label {
        flex: 1;
    }
</style>
