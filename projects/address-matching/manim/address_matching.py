from manim import *

# --- CONFIGURATION: Modern SaaS Dark Mode ---
# Nord-inspired palette for professional, modern aesthetics
BACKGROUND_COLOR = "#1e1e1e"  # Softer dark (not pure black)

# Primary role colors
DATA_COLOR = "#88C0D0"        # Nord Frost - Teal for data/addresses
BI_ENCODER_COLOR = "#B48EAD"  # Nord Aurora - Purple for models/encoders
CROSS_ENCODER_COLOR = "#5E81AC"  # Nord Frost - Deeper blue for cross-encoder
DB_COLOR = "#4C566A"          # Nord Polar - Gray for databases
EMBEDDING_COLOR = "#8FBCBB"   # Nord Frost - Lighter teal for embeddings
SUCCESS_COLOR = "#A3BE8C"     # Nord Aurora - Green for success/matching
ACCENT_COLOR = "#EBCB8B"      # Nord Aurora - Yellow/gold for highlights

# Typography
CLEAN_FONT = "Arial"  # Clean sans-serif with good Unicode support

# Standard corner radius for all shapes
CORNER_RADIUS = 0.2

class AddressMatchingArchitecture(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        
        # Helper to fix Cairo/Pango small font kerning issues by rendering large and scaling down
        def create_text(text, font_size=12, **kwargs):
            return Text(text, font_size=font_size * 4, **kwargs).scale(0.25)
        
        # --- TITLE --- (start centered, then shrink to corner)
        title = Text("Siamese Transformer Address Matching", font_size=42, font=CLEAN_FONT)
        subtitle = Text("Bi-encoder + Cross-encoder Architecture", font_size=26, color=GREY, font=CLEAN_FONT).next_to(title, DOWN, buff=0.15)
        title_group = VGroup(title, subtitle).move_to(ORIGIN)  # Centered on screen
        
        self.play(FadeIn(title_group, scale=0.9), run_time=0.8)
        self.wait(1.5)

        # --- PHASE 1: PRE-EMBEDDING (Figure 1) ---
        
        # Shrink and move title to top-left corner to make room
        small_title = create_text("Siamese Transformer", font_size=14, color=GREY, font=CLEAN_FONT).to_corner(UL, buff=0.15)
        self.play(
            ReplacementTransform(title_group, small_title),
            run_time=0.7
        )
        
        # Phase header - CENTERED
        header_1 = create_text("1. Database Pre-Embedding", font_size=28, color=DATA_COLOR, font=CLEAN_FONT).to_edge(UP, buff=0.4)
        self.play(FadeIn(header_1, shift=DOWN * 0.2), run_time=0.5)
        
        # Define 9 distinct colors for embeddings (Nord-inspired pastel palette)
        embedding_colors = [
            "#BF616A",  # Aurora Red
            "#D08770",  # Aurora Orange
            "#EBCB8B",  # Aurora Yellow
            "#A3BE8C",  # Aurora Green
            "#B48EAD",  # Aurora Purple
            "#88C0D0",  # Frost Teal
            "#81A1C1",  # Frost Blue
            "#5E81AC",  # Frost Deep Blue
            "#8FBCBB",  # Frost Light Teal
        ]
        
        # === BUILD ALL ELEMENTS FIRST, THEN ARRANGE FOR PROPER ALIGNMENT ===
        # Scale factor for fitting everything
        scale_factor = 0.8
        
        # 1. Create Address Table (ASCII-safe Portuguese addresses)
        all_addresses = [
            "Pc. de Espanha, N5, 1002",
            "Rua Bartolomeu Dias, LT82",
            "Praca do Comercio, 44",
            "...",
            "Av. de Roma, 12, 1Dto",
        ]
        
        # Table parameters (wider for cleaner text)
        table_width = 4.0
        row_height = 0.4
        header_height = 0.45
        
        # Helper function to create a table row (dark theme)
        def create_row(addr, idx):
            row_bg = RoundedRectangle(
                corner_radius=CORNER_RADIUS * 0.5,
                height=row_height, width=table_width,
                fill_color="#3B4252" if idx % 2 == 0 else "#434C5E",  # Nord Polar shades
                fill_opacity=1, stroke_color="#4C566A", stroke_width=0.5
            )
            # Larger font size for cleaner rendering
            row_text = create_text(addr, font_size=14, color="#ECEFF4", font=CLEAN_FONT).move_to(row_bg)  # Nord Snow
            return VGroup(row_bg, row_text)
        
        # Helper to build a complete table
        def build_table(addresses):
            header_bg = RoundedRectangle(
                corner_radius=CORNER_RADIUS,
                height=header_height, width=table_width, 
                fill_color=CROSS_ENCODER_COLOR, fill_opacity=1, stroke_color=DATA_COLOR, stroke_width=1
            )
            header_text = create_text("Addresses", font_size=12, color=WHITE, font=CLEAN_FONT).move_to(header_bg)
            header = VGroup(header_bg, header_text)
            
            rows = VGroup()
            for i, addr in enumerate(addresses):
                row = create_row(addr, i)
                rows.add(row)
            rows.arrange(DOWN, buff=0.05)
            header.next_to(rows, UP, buff=0)
            return VGroup(header, rows)
        
        # === ANIMATION FLOW: Database first, then table below, then compress into DB ===
        
        # LARGER scale for filling the screen
        scale_factor = 1.2
        
        # 2. Normalized Database - appears FIRST at the top-center (rounded corners)
        db_box = RoundedRectangle(
            corner_radius=CORNER_RADIUS,
            height=1.4, width=2.2, fill_color=DB_COLOR, fill_opacity=0.9, stroke_color=DATA_COLOR, stroke_width=2
        )
        db_label = VGroup(
            create_text("Normalized", font_size=16, color=WHITE, font=CLEAN_FONT),
            create_text("Database", font_size=16, color=WHITE, font=CLEAN_FONT)
        ).arrange(DOWN, buff=0.05).move_to(db_box)
        db_group = VGroup(db_box, db_label)
        db_group.scale(scale_factor)
        
        # Position database at top-center
        db_position = UP * 2.0
        db_group.move_to(db_position)
        
        # Show database first (slower)
        self.play(FadeIn(db_group, scale=0.8), run_time=0.8)
        self.wait(0.4)
        
        # === TABLE GENERATION BELOW DATABASE ===
        # Position for table (below the database)
        table_position = db_group.get_center() + DOWN * 2.5
        
        # Create table header first (larger, rounded)
        header_bg = RoundedRectangle(
            corner_radius=CORNER_RADIUS,
            height=header_height * 1.3, width=table_width * 1.2, 
            fill_color=CROSS_ENCODER_COLOR, fill_opacity=1, stroke_color=DATA_COLOR, stroke_width=1
        )
        header_text = create_text("Addresses", font_size=18, color=WHITE, font=CLEAN_FONT).move_to(header_bg)
        table_header = VGroup(header_bg, header_text)
        table_header.scale(scale_factor)
        table_header.move_to(table_position + UP * 0.8)
        
        # Show header (slower)
        self.play(FadeIn(table_header, shift=DOWN * 0.3), run_time=0.5)
        
        # Create rows first (position them all)
        table_rows = VGroup()
        for i, addr in enumerate(all_addresses):
            row = create_row(addr, i)
            row.scale(scale_factor)
            
            if i == 0:
                row.next_to(table_header, DOWN, buff=0.05)
            else:
                row.next_to(table_rows[-1], DOWN, buff=0.05)
            
            table_rows.add(row)
        
        # Use LaggedStart for smooth cascading appearance
        self.play(
            LaggedStart(*[
                FadeIn(row, shift=UP * 0.3)
                for row in table_rows
            ], lag_ratio=0.15, run_time=1.2)
        )
        
        self.wait(0.5)
        
        # Group the complete table
        complete_table = VGroup(table_header, table_rows)
        
        # === CASCADING MERGE COLLAPSE ANIMATION ===
        # Each row moves up and merges with the row above it
        
        rows_list = list(table_rows)
        
        # Start from the bottom row and merge upward
        for i in range(len(rows_list) - 1, 0, -1):
            current_row = rows_list[i]
            target_row = rows_list[i - 1]
            
            # Move current row up to merge with the row above (slowed down)
            self.play(
                current_row.animate(rate_func=smooth).move_to(target_row.get_center()).set_opacity(0.5),
                run_time=0.35
            )
            self.remove(current_row)
        
        # Now the first row merges with the header
        first_row = rows_list[0]
        self.play(
            first_row.animate(rate_func=smooth).move_to(table_header.get_center()).set_opacity(0.5),
            run_time=0.35
        )
        self.remove(first_row)
        
        # Finally, header merges into the database
        self.play(
            table_header.animate(rate_func=smooth).move_to(db_group.get_center()).scale(0.3).set_opacity(0),
            run_time=0.45
        )
        self.remove(table_header)
        
        # Pulse the database to show it received the data
        self.play(
            Indicate(db_group, color=WHITE, scale_factor=1.1),
            run_time=0.4
        )
        
        # Now move database to its pipeline position
        pipeline_y = DOWN * 0.6
        pipeline_db_pos = LEFT * 4.5 + pipeline_y  # Not too far left
        
        self.play(
            db_group.animate.move_to(pipeline_db_pos),
            run_time=0.7
        )
        
        # === BUILD REMAINING PIPELINE ELEMENTS ===
        # Smaller scale and more spacing to prevent overlap
        pipeline_scale = 0.85
        element_buff = 1.4  # More space between boxes for labels
        
        # 3. Bi-Encoder (compact, rounded with proper styling)
        bi_encoder = RoundedRectangle(
            corner_radius=CORNER_RADIUS, 
            height=0.9, width=1.4, fill_color=BI_ENCODER_COLOR, fill_opacity=0.9,
            stroke_color=DATA_COLOR, stroke_width=1.5
        )
        bi_label = create_text("Bi-Encoder", font_size=14, color=WHITE, font=CLEAN_FONT).move_to(bi_encoder)
        bi_group = VGroup(bi_encoder, bi_label)
        bi_group.scale(pipeline_scale)
        bi_group.next_to(db_group, RIGHT, buff=element_buff)
        bi_group.set_y(db_group.get_center()[1])
        
        # 4. Embeddings box (wider with labeled lines, rounded)
        emb_box = RoundedRectangle(
            corner_radius=CORNER_RADIUS,
            height=1.5, width=2.4, fill_color=CROSS_ENCODER_COLOR, fill_opacity=0.9, 
            stroke_color=DATA_COLOR, stroke_width=2
        )
        emb_title = create_text("Embeddings", font_size=14, color=WHITE, font=CLEAN_FONT)
        
        # Create 9 vertical lines (no labels)
        emb_lines = VGroup()
        for i, color in enumerate(embedding_colors):
            line = Line(UP * 0.4, DOWN * 0.4, color=color, stroke_width=4)
            emb_lines.add(line)
        
        # Arrange lines with more spacing
        emb_lines.arrange(RIGHT, buff=0.14).move_to(emb_box)
        
        emb_title.next_to(emb_box, UP, buff=0.1)
        emb_group = VGroup(emb_box, emb_lines, emb_title)
        emb_group.scale(pipeline_scale)
        emb_group.next_to(bi_group, RIGHT, buff=element_buff)
        emb_group.set_y(bi_group.get_center()[1])
        
        # 5. Auxiliary DB Grid (LARGER, rounded)
        aux_box = RoundedRectangle(
            corner_radius=CORNER_RADIUS,
            height=2.0, width=2.0, fill_color=CROSS_ENCODER_COLOR, fill_opacity=0.9, 
            stroke_color=DATA_COLOR, stroke_width=2
        )
        aux_title = VGroup(
            create_text("9 Auxiliary", font_size=14, color=DATA_COLOR, font=CLEAN_FONT),
            create_text("Databases", font_size=14, color=DATA_COLOR, font=CLEAN_FONT)
        ).arrange(DOWN, buff=0.03)
        
        # Use RoundedRectangle for grid cells too
        bins = VGroup()
        for i in range(9):
            b = RoundedRectangle(
                corner_radius=CORNER_RADIUS * 0.5,
                height=0.48, width=0.48, 
                fill_color=embedding_colors[i], fill_opacity=0.9, 
                stroke_color=WHITE, stroke_width=1
            )
            t = create_text(str(i + 1), font_size=14, color=WHITE, weight=BOLD, font=CLEAN_FONT).move_to(b)
            bins.add(VGroup(b, t))
        bins.arrange_in_grid(rows=3, cols=3, buff=0.08).move_to(aux_box)
        aux_title.next_to(aux_box, UP, buff=0.1)
        aux_group = VGroup(aux_box, aux_title, bins)
        aux_group.scale(pipeline_scale)
        aux_group.next_to(emb_group, RIGHT, buff=element_buff)
        aux_group.set_y(emb_group.get_center()[1])
        
        # === ANIMATE PIPELINE: DB -> Bi-Encoder -> Embeddings -> Aux DBs ===
        
        # Trapezoid connector: DB -> Bi-Encoder (replaces arrow)
        # Align trapezoid height with database and bi-encoder boxes
        db_right = db_group.get_right()
        bi_left = bi_group.get_left()
        trap_width = bi_left[0] - db_right[0] - 0.15  # Small gap between elements
        trap_center_x = (db_right[0] + bi_left[0]) / 2
        trap_center_y = db_group.get_center()[1]
        
        # Get the heights of database and bi-encoder boxes for trapezoid alignment
        db_height = db_group.get_height() * 0.6  # Narrower end near database
        bi_height = bi_group.get_height() * 0.9  # Wider end near bi-encoder
        
        # Create trapezoid aligned with box heights (narrow on left, wider on right)
        trap_db_bi_points = [
            [trap_center_x - trap_width/2 + 0.05, trap_center_y + db_height/2, 0],   # Top-left (narrow)
            [trap_center_x + trap_width/2 - 0.05, trap_center_y + bi_height/2, 0],    # Top-right (wide)
            [trap_center_x + trap_width/2 - 0.05, trap_center_y - bi_height/2, 0],   # Bottom-right
            [trap_center_x - trap_width/2 + 0.05, trap_center_y - db_height/2, 0], # Bottom-left
        ]
        trap_db_to_bi = Polygon(*trap_db_bi_points, fill_color=DATA_COLOR, fill_opacity=0.4, stroke_color=DATA_COLOR, stroke_width=2)
        
        self.play(FadeIn(trap_db_to_bi, shift=RIGHT * 0.2), run_time=0.6)
        self.play(FadeIn(bi_group), run_time=0.6)
        
        # Bi-encoder pulse animation to show processing
        self.play(
            bi_encoder.animate.scale(1.1).set_stroke(width=3),
            run_time=0.2
        )
        self.play(
            bi_encoder.animate.scale(1/1.1).set_stroke(width=1.5),
            run_time=0.2
        )
        
        # Arrow: Bi-Encoder -> Embeddings
        arrow_bi_to_emb = Arrow(bi_group.get_right(), emb_group.get_left(), buff=0.1, color=DATA_COLOR, stroke_width=2, max_tip_length_to_length_ratio=0.08)
        label_store = create_text("store", font_size=16, color=ACCENT_COLOR, weight=BOLD).next_to(arrow_bi_to_emb, DOWN, buff=0.12)
        
        self.play(GrowArrow(arrow_bi_to_emb), FadeIn(label_store), run_time=0.6)
        self.play(FadeIn(emb_box), FadeIn(emb_title), run_time=0.5)
        
        # Animate lines appearing with growing effect
        self.play(
            LaggedStart(*[
                GrowFromCenter(line) for line in emb_lines
            ], lag_ratio=0.1, run_time=0.8)
        )
        
        self.wait(0.3)
        
        # Arrow: Embeddings -> Aux DBs
        arrow_emb_to_aux = Arrow(emb_group.get_right(), aux_group.get_left(), buff=0.1, color=DATA_COLOR, stroke_width=2, max_tip_length_to_length_ratio=0.08)
        label_partition = create_text("partition", font_size=16, color=ACCENT_COLOR, weight=BOLD).next_to(arrow_emb_to_aux, DOWN, buff=0.12)
        
        self.play(GrowArrow(arrow_emb_to_aux), FadeIn(label_partition), run_time=0.6)
        # Show aux box, title, and all bins together
        self.play(FadeIn(aux_box), FadeIn(aux_title), FadeIn(bins), run_time=0.5)
        
        self.wait(0.5)
        
        # Store references for cleanup
        arrow_labels = VGroup(label_store, label_partition)
        phase1_arrows = VGroup(trap_db_to_bi, arrow_bi_to_emb, arrow_emb_to_aux)
        
        self.wait(1)

        # --- TRANSITION TO PHASE 2 ---
        # Fade out Phase 1 elements
        self.play(
            FadeOut(header_1), 
            FadeOut(small_title),
            FadeOut(phase1_arrows), FadeOut(arrow_labels),
            FadeOut(db_group), FadeOut(bi_group),
            FadeOut(emb_group)
        )

        # --- PHASE 2: PREDICTING MODULE ---
        # Layout matches the reference image exactly:
        # - Aux Databases (3x3 grid) at TOP CENTER
        # - Arrow pointing DOWN
        # - Cosine-Similarity Search box BELOW
        # - E1 embedding arrow coming from LEFT into the search box
        
        header_2 = create_text("2. Predicting Module", font_size=28, color=DATA_COLOR, font=CLEAN_FONT).to_edge(UP, buff=0.4)
        self.play(FadeIn(header_2, shift=DOWN * 0.2), run_time=0.5)
        
        # === POSITION AUX DATABASES AT TOP CENTER ===
        # Scale and position aux_group to be prominent at top-center
        self.play(
            aux_group.animate.scale(1.0).move_to(UP * 1.5 + RIGHT * 2)
        )
        
        # No "Aux Databases" label per Phase 2 requirements
        
        # === LEFT SIDE: INPUT → BI-ENCODER → E1 ===
        
        # 1. First show the Un-Normalized Address box (rounded, dark theme)
        input_box = RoundedRectangle(
            corner_radius=CORNER_RADIUS,
            height=0.9, width=3.4, fill_color=CROSS_ENCODER_COLOR, fill_opacity=0.9, 
            stroke_color=DATA_COLOR, stroke_width=2
        )
        input_label = VGroup(
            create_text("Un-Normalized Address (", font_size=13, color=WHITE, font=CLEAN_FONT),
            MathTex(r"x_1", font_size=16, color=WHITE),
            create_text(")", font_size=13, color=WHITE, font=CLEAN_FONT)
        ).arrange(RIGHT, buff=0.05).move_to(input_box)
        input_group = VGroup(input_box, input_label)
        input_group.move_to(LEFT * 4.5 + DOWN * 0.8)
        
        # Show the input box first
        self.play(FadeIn(input_group, scale=0.9), run_time=0.5)
        self.wait(0.3)
        
        # 2. Create sample address label above the input box with actual address
        sample_address_str = "Rua Pinheiro Manso, Nº10, 3001-234"
        sample_address_text = create_text(sample_address_str, font_size=12, color=WHITE, font=CLEAN_FONT)
        sample_address_bg = RoundedRectangle(
            corner_radius=CORNER_RADIUS * 0.5,
            height=0.5, width=3.6,
            fill_color="#3B4252", fill_opacity=1, 
            stroke_color=DATA_COLOR, stroke_width=1
        )
        sample_address_text.move_to(sample_address_bg)
        sample_address_label = VGroup(sample_address_bg, sample_address_text)
        sample_address_label.next_to(input_group, UP, buff=0.8)
        
        self.play(FadeIn(sample_address_label, shift=DOWN * 0.2), run_time=0.6)
        self.wait(0.4)
        
        # 3. Arrow from sample address to input box
        arrow_feed = Arrow(sample_address_label.get_bottom(), input_group.get_top(), buff=0.1, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        self.play(GrowArrow(arrow_feed), run_time=0.4)
        
        # 4. Animate sample address merging into input box - use FadeOut for complete removal
        self.play(
            FadeOut(sample_address_label, shift=DOWN * 0.5, scale=0.3),
            FadeOut(arrow_feed, shift=DOWN * 0.3),
            FadeOut(input_label),  # Remove original label at the same time
            run_time=0.6
        )
        
        # Show the full address in the input box
        full_address = create_text("Rua Pinheiro Manso, Nº10, 3001-234", font_size=13, color=WHITE, font=CLEAN_FONT)
        full_address.move_to(input_box.get_center())
        self.play(FadeIn(full_address), run_time=0.3)
        
        # Update reference for cleanup
        trapezoid_group = VGroup(full_address)
        
        # 5. Bi-Encoder to the right of input (consistent styling)
        bi_encoder_2 = RoundedRectangle(
            corner_radius=CORNER_RADIUS, 
            height=0.9, width=1.6, fill_color=BI_ENCODER_COLOR, fill_opacity=0.9, 
            stroke_color=DATA_COLOR, stroke_width=2
        )
        bi_label_2 = create_text("Bi-Encoder", font_size=14, color=WHITE, font=CLEAN_FONT).move_to(bi_encoder_2)
        bi_group_2 = VGroup(bi_encoder_2, bi_label_2)
        bi_group_2.next_to(input_group, RIGHT, buff=0.6)
        
        # Trapezoid connector from input to bi-encoder (replaces arrow)
        input_right = input_group.get_right()
        bi2_left = bi_group_2.get_left()
        trap2_width = bi2_left[0] - input_right[0] - 0.15
        trap2_center_x = (input_right[0] + bi2_left[0]) / 2
        trap2_center_y = input_group.get_center()[1]
        
        input_height = input_group.get_height() * 0.6
        bi2_height = bi_group_2.get_height() * 0.9
        
        trap2_points = [
            [trap2_center_x - trap2_width/2 + 0.05, trap2_center_y + input_height/2, 0],
            [trap2_center_x + trap2_width/2 - 0.05, trap2_center_y + bi2_height/2, 0],
            [trap2_center_x + trap2_width/2 - 0.05, trap2_center_y - bi2_height/2, 0],
            [trap2_center_x - trap2_width/2 + 0.05, trap2_center_y - input_height/2, 0],
        ]
        trap_input_to_bi = Polygon(*trap2_points, fill_color=DATA_COLOR, fill_opacity=0.4, stroke_color=DATA_COLOR, stroke_width=2)
        
        self.play(FadeIn(trap_input_to_bi, shift=RIGHT * 0.2), run_time=0.3)
        self.play(FadeIn(bi_group_2), run_time=0.4)
        
        # Bi-encoder pulse animation
        self.play(bi_encoder_2.animate.scale(1.1).set_stroke(width=3), run_time=0.15)
        self.play(bi_encoder_2.animate.scale(1/1.1).set_stroke(width=2), run_time=0.15)

        # 6. E1 Embedding - emerges from bi-encoder as a line (use query embedding color)
        query_color = "#BF616A"  # Aurora Red for query embedding
        e1_internal = Line(UP*0.12, DOWN*0.12, color=query_color, stroke_width=4).move_to(bi_encoder_2.get_center())
        self.play(GrowFromCenter(e1_internal), run_time=0.25)
        
        # E1 appears to the right of bi-encoder (keep at original position)
        e1_vec = Line(UP*0.25, DOWN*0.25, color=query_color, stroke_width=4)
        e1_vec.next_to(bi_group_2, RIGHT, buff=0.5)
        
        arrow_to_e1 = Arrow(bi_group_2.get_right(), e1_vec.get_left(), buff=0.1, color=DATA_COLOR, stroke_width=2, max_tip_length_to_length_ratio=0.08)
        
        self.play(GrowArrow(arrow_to_e1), run_time=0.3)
        self.play(ReplacementTransform(e1_internal, e1_vec), run_time=0.4)
        
        e1_label = MathTex(r"E_1", font_size=20, color=query_color).next_to(e1_vec, UP, buff=0.1)
        self.play(FadeIn(e1_label), run_time=0.25)
        
        e1_group = VGroup(e1_vec, e1_label)
        # Keep E1 at its original output position - no recentering
        
        # === COSINE-SIMILARITY SEARCH BOX - BELOW AUX DATABASES (with scanning visual) ===
        compare_box = RoundedRectangle(
            corner_radius=CORNER_RADIUS,
            height=1.0, width=2.6, fill_color=CROSS_ENCODER_COLOR, fill_opacity=0.9, 
            stroke_color=DATA_COLOR, stroke_width=2
        )
        compare_text = create_text("Cosine-Similarity\nSearch", font_size=14, color=WHITE, font=CLEAN_FONT).move_to(compare_box)
        compare_group = VGroup(compare_box, compare_text)
        compare_group.next_to(aux_group, DOWN, buff=0.8)
        
        # Arrow from Aux Databases DOWN to Search box
        arrow_aux_to_search = Arrow(
            aux_group.get_bottom(), 
            compare_group.get_top(), 
            buff=0.1, 
            color=DATA_COLOR, 
            stroke_width=2, 
            max_tip_length_to_length_ratio=0.08
        )
        
        self.play(GrowArrow(arrow_aux_to_search), run_time=0.4)
        self.play(FadeIn(compare_group), run_time=0.4)
        
        # Arrow from E1 to Search box (diagonal - E1 stays at original position)
        arrow_e1_to_search = Arrow(
            e1_vec.get_right(), 
            compare_group.get_left(), 
            buff=0.1, 
            color=query_color, 
            stroke_width=2, 
            max_tip_length_to_length_ratio=0.08
        )
        
        self.play(GrowArrow(arrow_e1_to_search), run_time=0.4)
        
        # Scanning effect animation - visual metaphor for similarity search
        scanner = Line(compare_box.get_top(), compare_box.get_bottom(), color=ACCENT_COLOR, stroke_width=6)
        scanner.move_to(compare_box.get_left() + RIGHT * 0.2)
        self.play(FadeIn(scanner, scale=0.5), run_time=0.1)
        self.play(
            scanner.animate.move_to(compare_box.get_right() + LEFT * 0.2),
            run_time=0.6,
            rate_func=smooth
        )
        self.play(FadeOut(scanner), run_time=0.1)
        
        # Make the entire search box turn golden to represent completion
        self.play(
            compare_box.animate.set_fill(ACCENT_COLOR, opacity=0.9).set_stroke(ACCENT_COLOR, width=3),
            run_time=0.4
        )
        
        # Flash to show comparison complete
        self.play(Indicate(compare_group, color=WHITE, scale_factor=1.05), run_time=0.3)

        # === TOP 10 CANDIDATES (rounded, styled) ===
        candidates_box = RoundedRectangle(
            corner_radius=CORNER_RADIUS,
            height=1.0, width=1.4, fill_color=DB_COLOR, fill_opacity=1, 
            stroke_color=DATA_COLOR, stroke_width=2
        )
        c_text = create_text("Top 10\nPairs", font_size=14, color=WHITE, font=CLEAN_FONT).move_to(candidates_box)
        c_group = VGroup(candidates_box, c_text)
        c_group.next_to(compare_group, RIGHT, buff=0.6)
        
        arrow_to_candidates = Arrow(compare_group.get_right(), c_group.get_left(), buff=0.1, color=DATA_COLOR, stroke_width=2, max_tip_length_to_length_ratio=0.08)
        self.play(GrowArrow(arrow_to_candidates), FadeIn(c_group), run_time=0.5)
        self.wait(1)

        # --- TRANSITION TO PHASE 3 (RE-RANKING) ---
        objects_to_fade = [
            header_2, trapezoid_group, input_box,
            bi_group_2, trap_input_to_bi, arrow_to_e1,
            e1_group, arrow_aux_to_search, arrow_e1_to_search,
            compare_group, arrow_to_candidates,
            aux_group
        ]
        
        self.play(*[FadeOut(obj) for obj in objects_to_fade])
        
        # --- PHASE 3: RERANKING ---
        header_3 = create_text("3. Re-Ranking Module", font_size=28, color=DATA_COLOR, font=CLEAN_FONT).to_edge(UP, buff=0.4)
        self.play(FadeIn(header_3, shift=DOWN * 0.2), run_time=0.5)
        
        # === ORIGINAL ADDRESS AT TOP CENTER (matching image layout) ===
        original_address_text = "Rua Pinheiro Manso, Nº10, 3001-234"
        original_label = create_text(original_address_text, font_size=18, color=WHITE, font=CLEAN_FONT)
        original_label.move_to(UP * 2.0)
        
        self.play(FadeIn(original_label, shift=DOWN * 0.2), run_time=0.5)
        self.wait(0.3)
        
        # === LAYOUT MATCHING THE IMAGE ===
        # Top-10 Pairs box on the LEFT
        # Trapezoid connector pointing to table on the RIGHT
        
        # === CREATE TRAPEZOID CONNECTOR (pointing right toward table) ===
        # Trapezoid with wider end on right (toward table)
        trap_points = [
            [-0.8, 0.35, 0],   # Top-left (narrower, near Top-10 box)
            [0.8, 0.5, 0],    # Top-right (wider, toward table)
            [0.8, -0.5, 0],   # Bottom-right
            [-0.8, -0.35, 0], # Bottom-left
        ]
        trapezoid_connector = Polygon(*trap_points, fill_color=CROSS_ENCODER_COLOR, fill_opacity=0.9, stroke_color=DATA_COLOR, stroke_width=2)
        # Position trapezoid at center of screen horizontally
        trapezoid_connector.move_to(ORIGIN + DOWN * 0.3)
        
        # Move the Top-10 Pairs box to the left of the trapezoid
        self.play(c_group.animate.next_to(trapezoid_connector, LEFT, buff=0.1), run_time=0.5)
        
        self.play(FadeIn(trapezoid_connector, shift=RIGHT * 0.2), run_time=0.4)
        
        # === CREATE TABLE WITH ADDRESSES (matching image format) ===
        # Show all 9 candidate addresses from the Top-10 pairs
        candidate_row_height = 0.4
        candidate_row_width = 3.2  # Slightly narrower to fit centered layout
        
        # Animation spacing - space on left/right for slide-out animations
        # Slide out fully: one bar width + small gap so there's clear space between sliding element and table
        slide_offset = candidate_row_width + 0.2
        
        # Addresses in initial order (unsorted, before reranking) - with zip codes
        # The correct match "Rua Pinheiro Manso, Nº10, 3001-234" will be at index 6
        initial_addresses = [
            ("R Pinheiro Manso, N1, 3001-100", 0.75),              # Medium match
            ("R Pinheiro Manso, N10, 3001-235", 0.88),             # Good match
            ("Rua Pinheiro Manso, LT5, 3001-234", 0.72),           # Slightly different
            ("R P. Manso, 10, 3001-234", 0.82),                    # Abbreviated version
            ("Av. Pinheiro Manso, N10, 3002-100", 0.68),           # Wrong street type
            ("Rua Pinheiros, Nº10, 4000-123", 0.55),               # Partial match
            ("Rua Pinheiro Manso, Nº10, 3001-234", 0.98),          # BEST match (correct)
            ("R Pinheiro Bravo, LT4, 3001-567", 0.45),             # Poor match
            ("R dos Pinheiros, 23, 4500-890", 0.32),               # Worst match
        ]
        
        # Helper to create candidate row (dark theme for consistency)
        def create_table_row(addr, idx):
            row_bg = RoundedRectangle(
                corner_radius=CORNER_RADIUS * 0.5,
                height=candidate_row_height, width=candidate_row_width,
                fill_color="#3B4252" if idx % 2 == 0 else "#434C5E",  # Nord Polar
                fill_opacity=1, stroke_color="#4C566A", stroke_width=0.5
            )
            row_text = create_text(addr, font_size=12, color="#ECEFF4", font=CLEAN_FONT).move_to(row_bg)  # Nord Snow
            return VGroup(row_bg, row_text)
        
        # Table header (rounded)
        table_header_bg = RoundedRectangle(
            corner_radius=CORNER_RADIUS,
            height=candidate_row_height + 0.05, width=candidate_row_width,
            fill_color=CROSS_ENCODER_COLOR, fill_opacity=1, stroke_color=DATA_COLOR, stroke_width=1
        )
        table_header_text = create_text("Candidate Addresses", font_size=11, color=WHITE, font=CLEAN_FONT).move_to(table_header_bg)
        table_header = VGroup(table_header_bg, table_header_text)
        
        # Calculate table center position: align middle of table with trapezoid center
        num_rows = len(initial_addresses)
        row_gap = 0.03
        total_table_height = (candidate_row_height + 0.05) + (num_rows * (candidate_row_height + row_gap))
        trapezoid_center_y = trapezoid_connector.get_center()[1]
        table_center_y = trapezoid_center_y  # Align centers
        
        # Position header so the whole table is centered vertically with trapezoid
        # Use same gap (0.1) as between Top-10 box and trapezoid
        table_top_y = table_center_y + total_table_height / 2
        table_header.move_to([trapezoid_connector.get_right()[0] + 0.1 + candidate_row_width / 2, 
                              table_top_y - (candidate_row_height + 0.05) / 2, 0])
        
        self.play(FadeIn(table_header, shift=RIGHT * 0.15), run_time=0.3)
        
        # Create and animate rows appearing one by one
        # Use separate dictionaries to track scores and addresses
        candidate_rows = VGroup()
        row_scores = {}  # index -> score
        row_addresses = {}  # index -> address
        
        for i, (addr, score) in enumerate(initial_addresses):
            row = create_table_row(addr, i)
            
            if i == 0:
                row.next_to(table_header, DOWN, buff=0.03)
            else:
                row.next_to(candidate_rows[-1], DOWN, buff=0.03)
            
            candidate_rows.add(row)
            row_scores[i] = score
            row_addresses[i] = addr
            
        # Use LaggedStart for smoother table appearance
        self.play(
            LaggedStart(*[
                FadeIn(row, shift=DOWN * 0.12)
                for row in candidate_rows
            ], lag_ratio=0.08, run_time=1.0)
        )
        
        self.wait(0.5)
        
        # Group the table parts
        table_group = VGroup(table_header, candidate_rows)
        
        # === RERANKING ANIMATION WITH INSERTION-SORT STYLE ===
        # Visual indicator of processing
        self.play(Indicate(table_group, color=ACCENT_COLOR, scale_factor=1.02), run_time=0.3)
        
        # Store slot positions
        slot_positions = [candidate_rows[i].get_center().copy() for i in range(len(candidate_rows))]
        
        # Animation speed
        anim_speed = 0.15
        
        # Highlight color for moving elements
        highlight_color = ACCENT_COLOR
        
        # Get sorted order (hardcoded based on scores):
        # idx 6 (0.98) → slot 0, idx 1 (0.88) → slot 1, idx 3 (0.82) → slot 2
        # idx 0 (0.75) → slot 3, idx 2 (0.72) → slot 4, idx 4 (0.68) → slot 5
        # idx 5 (0.55) → slot 6, idx 7 (0.45) → slot 7, idx 8 (0.32) → slot 8
        sorted_by_score = [
            (6, candidate_rows[6]), (1, candidate_rows[1]), (3, candidate_rows[3]),
            (0, candidate_rows[0]), (2, candidate_rows[2]), (4, candidate_rows[4]),
            (5, candidate_rows[5]), (7, candidate_rows[7]), (8, candidate_rows[8])
        ]
        
        # Helper function for swap animation
        def animate_swap(row_a, slot_a, row_b, slot_b, direction_a=RIGHT):
            """Animate swapping row_a (going to slot_b's position) with row_b (going to slot_a's position)"""
            direction_b = LEFT if direction_a is RIGHT else RIGHT
            
            # Highlight row_a
            self.play(row_a[0].animate.set_stroke(color=highlight_color, width=3), run_time=anim_speed * 0.5)
            
            # Both slide out simultaneously
            self.play(
                row_a.animate.shift(direction_a * slide_offset),
                row_b.animate.shift(direction_b * slide_offset),
                run_time=anim_speed
            )
            
            # Both move vertically to swap positions
            self.play(
                row_a.animate.move_to([row_a.get_center()[0], slot_positions[slot_b][1], 0]),
                row_b.animate.move_to([row_b.get_center()[0], slot_positions[slot_a][1], 0]),
                run_time=anim_speed
            )
            
            # Both slide back in
            self.play(
                row_a.animate.move_to(slot_positions[slot_b]),
                row_b.animate.move_to(slot_positions[slot_a]),
                run_time=anim_speed
            )
            
            # Remove highlight
            self.play(row_a[0].animate.set_stroke(color="#4C566A", width=0.5), run_time=anim_speed * 0.3)
        
        # === HARDCODED SWAP SEQUENCE ===
        # Current state: [0, 1, 2, 3, 4, 5, 6, 7, 8] at slots [0, 1, 2, 3, 4, 5, 6, 7, 8]
        # Target state:  [6, 1, 3, 0, 2, 4, 5, 7, 8]
        
        # Swap 1: Move idx 6 to slot 0 (swap with idx 0)
        # After: [6, 1, 2, 3, 4, 5, 0, 7, 8]
        animate_swap(candidate_rows[6], 6, candidate_rows[0], 0, RIGHT)
        
        # Swap 2: Move idx 3 to slot 2 (swap with idx 2)
        # After: [6, 1, 3, 2, 4, 5, 0, 7, 8]
        animate_swap(candidate_rows[3], 3, candidate_rows[2], 2, LEFT)
        
        # Swap 3: Move idx 0 (now at slot 6) to slot 3 (swap with idx 2 now at slot 3)
        # After: [6, 1, 3, 0, 4, 5, 2, 7, 8]
        animate_swap(candidate_rows[0], 6, candidate_rows[2], 3, RIGHT)
        
        # Swap 4: Move idx 2 (now at slot 6) to slot 4 (swap with idx 4)
        # After: [6, 1, 3, 0, 2, 5, 4, 7, 8]
        animate_swap(candidate_rows[2], 6, candidate_rows[4], 4, LEFT)
        
        # Swap 5: Move idx 4 (now at slot 6) to slot 5 (swap with idx 5)
        # After: [6, 1, 3, 0, 2, 4, 5, 7, 8] - SORTED!
        animate_swap(candidate_rows[4], 6, candidate_rows[5], 5, RIGHT)
        
        # Brief pause to show sorted state
        self.wait(0.3)
        
        # === HIGHLIGHT THE TOP ROW (BEST MATCH) ===
        best_match_idx = sorted_by_score[0][0]  # Original index of best match
        best_match_row = sorted_by_score[0][1]  # First in sorted order = best match
        best_match_address = row_addresses[best_match_idx]
        
        # Create highlight border with SUCCESS_COLOR
        highlight_rect = RoundedRectangle(
            corner_radius=CORNER_RADIUS * 0.5,
            height=candidate_row_height + 0.1, width=candidate_row_width + 0.1,
            stroke_color=SUCCESS_COLOR, stroke_width=4, fill_opacity=0
        ).move_to(best_match_row)
        
        self.play(Create(highlight_rect), run_time=0.4)
        
        # Change the row to green styling with rounded corners
        best_match_new_bg = RoundedRectangle(
            corner_radius=CORNER_RADIUS * 0.5,
            height=candidate_row_height, width=candidate_row_width,
            fill_color="#2E5939", fill_opacity=1,  # Dark green background
            stroke_color=SUCCESS_COLOR, stroke_width=2
        ).move_to(best_match_row)
        best_match_new_text = create_text(best_match_address, font_size=13, color=WHITE, font=CLEAN_FONT).move_to(best_match_new_bg)
        best_match_styled = VGroup(best_match_new_bg, best_match_new_text)
        
        # Track which rows to fade out BEFORE the transform (exclude best_match_row)
        rows_to_fade = [candidate_rows[i] for i in range(len(candidate_rows)) if i != best_match_idx]
        
        self.play(
            ReplacementTransform(best_match_row, best_match_styled),
            run_time=0.4
        )
        
        # Flash effect to signify the final match!
        self.play(
            Flash(
                best_match_styled,
                color=SUCCESS_COLOR,
                line_length=0.4,
                num_lines=16,
                flash_radius=1.0,
                run_time=0.6
            )
        )
        
        self.play(Indicate(best_match_styled, color=SUCCESS_COLOR, scale_factor=1.05), run_time=0.3)
        
        # Add "Best Match" label
        best_label = Text("← Best Match (98%)", font_size=14, color=SUCCESS_COLOR, font=CLEAN_FONT)
        best_label.next_to(best_match_styled, RIGHT, buff=0.2)
        self.play(FadeIn(best_label, shift=LEFT * 0.1), run_time=0.3)
        
        self.wait(0.5)
        
        # === COLLAPSE TABLE TO SHOW ONLY CORRECT MATCH ===
        self.play(
            *[FadeOut(row) for row in rows_to_fade],  # Fade all rows except best match
            FadeOut(table_header),
            FadeOut(trapezoid_connector),
            FadeOut(c_group),
            FadeOut(highlight_rect),
            FadeOut(best_label),
            run_time=0.6
        )
        
        # Move the correct row to center, below the original address
        self.play(best_match_styled.animate.move_to(ORIGIN + DOWN * 0.3), run_time=0.5)
        
        # Add "Matched Address" label
        match_label = create_text("Matched Address", font_size=16, color="#4CAF50", font=CLEAN_FONT)
        match_label.next_to(best_match_styled, UP, buff=0.2)
        self.play(FadeIn(match_label), run_time=0.3)
        
        # === COMPARISON ANIMATION ===
        # Draw comparison arrow between original and match
        comparison_arrow = DoubleArrow(
            original_label.get_bottom(), 
            match_label.get_top(), 
            buff=0.15, 
            color=SUCCESS_COLOR, 
            stroke_width=3,
            max_tip_length_to_length_ratio=0.08
        )
        
        self.play(GrowArrow(comparison_arrow), run_time=0.5)
        
        # Highlight matching with styled text
        comparison_label = create_text("Matched!", font_size=22, color=SUCCESS_COLOR, font=CLEAN_FONT)
        comparison_label.next_to(comparison_arrow, RIGHT, buff=0.4)
        
        self.play(FadeIn(comparison_label, scale=1.2), run_time=0.4)
        
        # Final flash on both addresses
        self.play(
            Indicate(original_label, color=SUCCESS_COLOR, scale_factor=1.05),
            Indicate(best_match_styled, color=SUCCESS_COLOR, scale_factor=1.05),
            run_time=0.5
        )
        
        self.wait(2)