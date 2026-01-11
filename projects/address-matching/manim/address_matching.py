from manim import *

# --- CONFIGURATION ---
BI_ENCODER_COLOR = PURPLE_B
CROSS_ENCODER_COLOR = BLUE_D
DB_COLOR = GREY_D
EMBEDDING_COLOR = TEAL_C
BACKGROUND_COLOR = "#101010"
# Use Sans font for better letter spacing (Arial can cause issues on some systems)
CLEAN_FONT = "Sans"

class AddressMatchingArchitecture(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        
        # --- TITLE --- (start centered, then shrink to corner)
        title = Text("Siamese Transformer Address Matching", font_size=42, font=CLEAN_FONT)
        subtitle = Text("Bi-encoder + Cross-encoder Architecture", font_size=26, color=GREY, font=CLEAN_FONT).next_to(title, DOWN, buff=0.15)
        title_group = VGroup(title, subtitle).move_to(ORIGIN)  # Centered on screen
        
        self.play(FadeIn(title_group, scale=0.9), run_time=0.8)
        self.wait(1.5)

        # --- PHASE 1: PRE-EMBEDDING (Figure 1) ---
        
        # Shrink and move title to top-left corner to make room
        small_title = Text("Siamese Transformer", font_size=14, color=GREY, font=CLEAN_FONT).to_corner(UL, buff=0.15)
        self.play(
            ReplacementTransform(title_group, small_title),
            run_time=0.7
        )
        
        # Phase header - CENTERED
        header_1 = Text("1. Database Pre-Embedding", font_size=28, color=BLUE, font=CLEAN_FONT).to_edge(UP, buff=0.4)
        self.play(FadeIn(header_1), run_time=0.5)
        
        # Define 9 distinct colors for embeddings (matching aux databases)
        embedding_colors = [
            "#FF6B6B",  # Red
            "#4ECDC4",  # Teal
            "#45B7D1",  # Sky Blue
            "#96CEB4",  # Sage Green
            "#FFEAA7",  # Yellow
            "#DDA0DD",  # Plum
            "#98D8C8",  # Mint
            "#F7DC6F",  # Gold
            "#BB8FCE",  # Lavender
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
        
        # Helper function to create a table row
        def create_row(addr, idx):
            row_bg = Rectangle(
                height=row_height, width=table_width,
                fill_color=WHITE if idx % 2 == 0 else "#E8E8E8",
                fill_opacity=1, stroke_color="#CCCCCC", stroke_width=0.5
            )
            # Larger font size for cleaner rendering
            row_text = Text(addr, font_size=14, color=BLACK, font=CLEAN_FONT).move_to(row_bg)
            return VGroup(row_bg, row_text)
        
        # Helper to build a complete table
        def build_table(addresses):
            header_bg = Rectangle(
                height=header_height, width=table_width, 
                fill_color="#2C5F7C", fill_opacity=1, stroke_color=WHITE, stroke_width=1
            )
            header_text = Text("Addresses", font_size=12, color=WHITE, font=CLEAN_FONT).move_to(header_bg)
            header = VGroup(header_bg, header_text)
            
            rows = VGroup()
            for i, addr in enumerate(addresses):
                row = create_row(addr, i)
                rows.add(row)
            rows.arrange(DOWN, buff=0)
            header.next_to(rows, UP, buff=0)
            return VGroup(header, rows)
        
        # === ANIMATION FLOW: Database first, then table below, then compress into DB ===
        
        # LARGER scale for filling the screen
        scale_factor = 1.2
        
        # 2. Normalized Database - appears FIRST at the top-center
        db_box = Rectangle(height=1.4, width=2.2, fill_color=DB_COLOR, fill_opacity=0.8, stroke_color=WHITE, stroke_width=2)
        db_label = VGroup(
            Text("Normalized", font_size=16, color=WHITE, font=CLEAN_FONT),
            Text("Database", font_size=16, color=WHITE, font=CLEAN_FONT)
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
        
        # Create table header first (larger)
        header_bg = Rectangle(
            height=header_height * 1.3, width=table_width * 1.2, 
            fill_color="#2C5F7C", fill_opacity=1, stroke_color=WHITE, stroke_width=1
        )
        header_text = Text("Addresses", font_size=18, color=WHITE, font=CLEAN_FONT).move_to(header_bg)
        table_header = VGroup(header_bg, header_text)
        table_header.scale(scale_factor)
        table_header.move_to(table_position + UP * 0.8)
        
        # Show header (slower)
        self.play(FadeIn(table_header, shift=DOWN * 0.3), run_time=0.5)
        
        # Create and animate rows appearing one by one below (slower)
        table_rows = VGroup()
        for i, addr in enumerate(all_addresses):
            row = create_row(addr, i)
            row.scale(scale_factor)
            
            if i == 0:
                row.next_to(table_header, DOWN, buff=0)
            else:
                row.next_to(table_rows[-1], DOWN, buff=0)
            
            table_rows.add(row)
            
            # Animate each row appearing (slower)
            self.play(FadeIn(row, shift=DOWN * 0.2), run_time=0.35)
        
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
            
            # Move current row up to merge with the row above
            self.play(
                current_row.animate(rate_func=smooth).move_to(target_row.get_center()).set_opacity(0.5),
                run_time=0.18
            )
            self.remove(current_row)
        
        # Now the first row merges with the header
        first_row = rows_list[0]
        self.play(
            first_row.animate(rate_func=smooth).move_to(table_header.get_center()).set_opacity(0.5),
            run_time=0.18
        )
        self.remove(first_row)
        
        # Finally, header merges into the database
        self.play(
            table_header.animate(rate_func=smooth).move_to(db_group.get_center()).scale(0.3).set_opacity(0),
            run_time=0.25
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
        
        # 3. Bi-Encoder (compact)
        bi_encoder = RoundedRectangle(corner_radius=0.1, height=0.9, width=1.4, fill_color=BI_ENCODER_COLOR, fill_opacity=0.8)
        bi_label = Text("Bi-Encoder", font_size=14, color=WHITE, font=CLEAN_FONT).move_to(bi_encoder)
        bi_group = VGroup(bi_encoder, bi_label)
        bi_group.scale(pipeline_scale)
        bi_group.next_to(db_group, RIGHT, buff=element_buff)
        bi_group.set_y(db_group.get_center()[1])
        
        # 4. Embeddings box (wider with labeled lines)
        emb_box = Rectangle(height=1.5, width=2.4, fill_color="#2C5F7C", fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
        emb_title = Text("Embeddings", font_size=14, color=WHITE, font=CLEAN_FONT)
        
        # Create 9 vertical lines with labels e_1, e_2, etc.
        emb_lines = VGroup()
        emb_labels = VGroup()
        for i, color in enumerate(embedding_colors):
            line = Line(UP * 0.4, DOWN * 0.4, color=color, stroke_width=4)
            # Create label for this embedding
            label = Text(f"e{i+1}", font_size=8, color=color)
            emb_lines.add(line)
            emb_labels.add(label)
        
        # Arrange lines with more spacing
        emb_lines.arrange(RIGHT, buff=0.14).move_to(emb_box)
        
        # Position labels below each line
        for i, (line, label) in enumerate(zip(emb_lines, emb_labels)):
            label.next_to(line, DOWN, buff=0.06)
        
        emb_title.next_to(emb_box, UP, buff=0.1)
        emb_group = VGroup(emb_box, emb_lines, emb_labels, emb_title)
        emb_group.scale(pipeline_scale)
        emb_group.next_to(bi_group, RIGHT, buff=element_buff)
        emb_group.set_y(bi_group.get_center()[1])
        
        # 5. Auxiliary DB Grid (LARGER)
        aux_box = Rectangle(height=2.0, width=2.0, fill_color="#2C5F7C", fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
        aux_title = VGroup(
            Text("9 Auxiliary", font_size=14, color=WHITE, font=CLEAN_FONT),
            Text("Databases", font_size=14, color=WHITE, font=CLEAN_FONT)
        ).arrange(DOWN, buff=0.03)
        
        bins = VGroup()
        for i in range(9):
            b = Square(side_length=0.48, fill_color=embedding_colors[i], fill_opacity=0.8, stroke_color=WHITE, stroke_width=1)
            t = Text(str(i + 1), font_size=14, color=WHITE, weight=BOLD, font=CLEAN_FONT).move_to(b)
            bins.add(VGroup(b, t))
        bins.arrange_in_grid(rows=3, cols=3, buff=0.08).move_to(aux_box)
        aux_title.next_to(aux_box, UP, buff=0.1)
        aux_group = VGroup(aux_box, aux_title, bins)
        aux_group.scale(pipeline_scale)
        aux_group.next_to(emb_group, RIGHT, buff=element_buff)
        aux_group.set_y(emb_group.get_center()[1])
        
        # === ANIMATE PIPELINE: DB -> Bi-Encoder -> Embeddings -> Aux DBs ===
        
        # Arrow: DB -> Bi-Encoder (smaller label to fit spacing)
        arrow_db_to_bi = Arrow(db_group.get_right(), bi_group.get_left(), buff=0.1, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        label_encode = Text("bi-encode", font_size=16, color=YELLOW).next_to(arrow_db_to_bi, DOWN, buff=0.12)
        
        self.play(GrowArrow(arrow_db_to_bi), FadeIn(label_encode), run_time=0.6)
        self.play(FadeIn(bi_group), run_time=0.6)
        
        # Brief encoding animation
        for _ in range(2):
            dot = Dot(color=YELLOW, radius=0.05).move_to(db_group.get_right())
            self.play(dot.animate.move_to(bi_group.get_center()).set_opacity(0), run_time=0.3)
            self.remove(dot)
        
        # Arrow: Bi-Encoder -> Embeddings
        arrow_bi_to_emb = Arrow(bi_group.get_right(), emb_group.get_left(), buff=0.1, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        label_store = Text("store", font_size=16, color=YELLOW).next_to(arrow_bi_to_emb, DOWN, buff=0.12)
        
        self.play(GrowArrow(arrow_bi_to_emb), FadeIn(label_store), run_time=0.6)
        self.play(FadeIn(emb_box), FadeIn(emb_title), run_time=0.5)
        
        # Animate lines appearing one by one
        for line in emb_lines:
            self.play(Create(line), run_time=0.12)
        
        self.wait(0.3)
        
        # Arrow: Embeddings -> Aux DBs
        arrow_emb_to_aux = Arrow(emb_group.get_right(), aux_group.get_left(), buff=0.1, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        label_partition = Text("partition", font_size=16, color=YELLOW).next_to(arrow_emb_to_aux, DOWN, buff=0.12)
        
        self.play(GrowArrow(arrow_emb_to_aux), FadeIn(label_partition), run_time=0.6)
        self.play(FadeIn(aux_box), FadeIn(aux_title), run_time=0.5)
        
        # === ANIMATE LINES DUPLICATING INTO 9 BOXES ===
        # Each embedding line duplicates and moves into its corresponding box
        for i, (line, bin_square) in enumerate(zip(emb_lines, bins)):
            # Create a copy of the line
            line_copy = line.copy()
            
            # Scale down the line copy and move it into the bin
            target_line = Line(UP * 0.12, DOWN * 0.12, color=embedding_colors[i], stroke_width=3)
            target_line.move_to(bin_square[0].get_center())
            
            # Animate the duplication
            self.play(
                ReplacementTransform(line_copy, target_line),
                FadeIn(bin_square),
                run_time=0.25
            )
            self.remove(target_line)  # The bin is now visible
        
        self.wait(0.5)
        
        # Store references for cleanup
        arrow_labels = VGroup(label_encode, label_store, label_partition)
        phase1_arrows = VGroup(arrow_db_to_bi, arrow_bi_to_emb, arrow_emb_to_aux)
        
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
        
        header_2 = Text("2. Predicting Module", font_size=28, color=BLUE, font=CLEAN_FONT).to_edge(UP, buff=0.4)
        self.play(FadeIn(header_2), run_time=0.5)
        
        # === POSITION AUX DATABASES AT TOP CENTER ===
        # Scale and position aux_group to be prominent at top-center
        self.play(
            aux_group.animate.scale(1.0).move_to(UP * 1.5 + RIGHT * 2)
        )
        
        lbl_aux = Text("Aux Databases", font_size=16, color=WHITE, font=CLEAN_FONT).next_to(aux_group, UP, buff=0.15)
        self.play(FadeIn(lbl_aux), run_time=0.3)
        
        # === LEFT SIDE: INPUT → BI-ENCODER → E1 ===
        # Similar table animation as Phase 1 for un-normalized addresses
        
        # 1. First show the Un-Normalized Address box (like the database in Phase 1)
        input_box = Rectangle(height=0.9, width=3.4, fill_color="#2C5F7C", fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
        input_label = Text("Un-Normalized Address (x₁)", font_size=13, color=WHITE, font=CLEAN_FONT).move_to(input_box)
        input_group = VGroup(input_box, input_label)
        input_group.move_to(LEFT * 4.5 + DOWN * 0.8)
        
        # Show the input box first (like the database)
        self.play(FadeIn(input_group, scale=0.9), run_time=0.5)
        self.wait(0.3)
        
        # 2. Create trapezoid header above the input box (like table header)
        trapezoid_points = [
            [-2.2, 0.45, 0],   # Top-left (wider)
            [2.2, 0.45, 0],    # Top-right (wider)
            [1.8, -0.45, 0],   # Bottom-right
            [-1.8, -0.45, 0],  # Bottom-left
        ]
        trapezoid = Polygon(*trapezoid_points, fill_color="#2C5F7C", fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
        trapezoid_header_text = Text("Input Address", font_size=12, color=WHITE, font=CLEAN_FONT).move_to(trapezoid)
        trapezoid_header = VGroup(trapezoid, trapezoid_header_text)
        trapezoid_header.next_to(input_group, UP, buff=1.5)
        
        self.play(FadeIn(trapezoid_header, shift=DOWN * 0.2), run_time=0.4)
        
        # 3. Create address rows that appear one by one (like the table rows)
        address_row_height = 0.35
        address_row_width = 2.8
        
        # Helper to create an address row
        def create_input_row(addr, idx):
            row_bg = Rectangle(
                height=address_row_height, width=address_row_width,
                fill_color=WHITE if idx % 2 == 0 else "#E8E8E8",
                fill_opacity=1, stroke_color="#CCCCCC", stroke_width=0.5
            )
            row_text = Text(addr, font_size=11, color=BLACK, font=CLEAN_FONT).move_to(row_bg)
            return VGroup(row_bg, row_text)
        
        # The address to input (split into meaningful parts for visual effect)
        address_parts = [
            "Rua Pinheiro Manso",
            "Nº10",
            "3001-234",
        ]
        
        input_rows = VGroup()
        for i, part in enumerate(address_parts):
            row = create_input_row(part, i)
            
            if i == 0:
                row.next_to(trapezoid_header, DOWN, buff=0)
            else:
                row.next_to(input_rows[-1], DOWN, buff=0)
            
            input_rows.add(row)
            
            # Animate each row appearing
            self.play(FadeIn(row, shift=DOWN * 0.15), run_time=0.25)
        
        self.wait(0.3)
        
        # 4. Cascading merge animation (rows merge upward)
        rows_list = list(input_rows)
        
        # Start from the bottom row and merge upward
        for i in range(len(rows_list) - 1, 0, -1):
            current_row = rows_list[i]
            target_row = rows_list[i - 1]
            
            self.play(
                current_row.animate(rate_func=smooth).move_to(target_row.get_center()).set_opacity(0.5),
                run_time=0.15
            )
            self.remove(current_row)
        
        # First row merges with the trapezoid header
        first_row = rows_list[0]
        self.play(
            first_row.animate(rate_func=smooth).move_to(trapezoid_header.get_center()).set_opacity(0.5),
            run_time=0.15
        )
        self.remove(first_row)
        
        # 5. Trapezoid flows down into the input box
        # Create the full address text that will appear in the input box
        full_address = Text("Rua Pinheiro Manso, Nº10, 3001-234", font_size=13, color=WHITE, font=CLEAN_FONT)
        full_address.move_to(trapezoid_header.get_center())
        
        # Replace trapezoid content with full address
        self.play(
            FadeOut(trapezoid_header_text),
            FadeIn(full_address),
            run_time=0.2
        )
        
        # Arrow from trapezoid to input box
        arrow_feed = Arrow(trapezoid_header.get_bottom(), input_group.get_top(), buff=0.1, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        self.play(GrowArrow(arrow_feed), run_time=0.3)
        
        # Animate the address flowing into the input box while arrow shrinks
        self.play(
            full_address.animate(rate_func=smooth).move_to(input_box.get_center()).scale(0.95),
            trapezoid.animate(rate_func=smooth).move_to(input_group.get_center()).scale(0.3).set_opacity(0),
            arrow_feed.animate(rate_func=smooth).scale(0, about_point=input_group.get_top()).set_opacity(0),
            run_time=0.4
        )
        self.remove(trapezoid, arrow_feed)
        
        # Fade out the original label
        self.play(FadeOut(input_label), run_time=0.2)
        
        # Pulse the input box to show it received the data
        self.play(Indicate(input_group, color=WHITE, scale_factor=1.05), run_time=0.3)
        
        # Update trapezoid_group reference for cleanup (now it's just the address in the box)
        trapezoid_group = VGroup(full_address)
        
        # 3. Bi-Encoder to the right of input
        bi_encoder_2 = RoundedRectangle(corner_radius=0.15, height=0.9, width=1.6, fill_color=BI_ENCODER_COLOR, fill_opacity=0.8, stroke_color=WHITE, stroke_width=2)
        bi_label_2 = Text("Bi-Encoder", font_size=14, color=WHITE, font=CLEAN_FONT).move_to(bi_encoder_2)
        bi_group_2 = VGroup(bi_encoder_2, bi_label_2)
        bi_group_2.next_to(input_group, RIGHT, buff=0.6)
        
        arrow_input = Arrow(input_group.get_right(), bi_group_2.get_left(), buff=0.1, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        
        self.play(GrowArrow(arrow_input), run_time=0.3)
        self.play(FadeIn(bi_group_2), run_time=0.4)
        
        # Encoding animation
        for _ in range(2):
            dot = Dot(color=YELLOW, radius=0.05).move_to(input_group.get_right())
            self.play(dot.animate.move_to(bi_group_2.get_center()).set_opacity(0), run_time=0.2)
            self.remove(dot)

        # 4. E1 Embedding - emerges from bi-encoder as a line
        e1_internal = Line(UP*0.12, DOWN*0.12, color=RED, stroke_width=4).move_to(bi_encoder_2.get_center())
        self.play(Create(e1_internal), run_time=0.25)
        
        # E1 appears to the right of bi-encoder
        e1_vec = Line(UP*0.25, DOWN*0.25, color=RED, stroke_width=4)
        e1_vec.next_to(bi_group_2, RIGHT, buff=0.5)
        
        arrow_to_e1 = Arrow(bi_group_2.get_right(), e1_vec.get_left(), buff=0.1, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        
        self.play(GrowArrow(arrow_to_e1), run_time=0.3)
        self.play(ReplacementTransform(e1_internal, e1_vec), run_time=0.4)
        
        e1_label = Text("E₁", font_size=16, color=RED, font=CLEAN_FONT).next_to(e1_vec, UP, buff=0.1)
        self.play(FadeIn(e1_label), run_time=0.25)
        
        e1_group = VGroup(e1_vec, e1_label)
        
        # === COSINE-SIMILARITY SEARCH BOX - BELOW AUX DATABASES ===
        # Positioned exactly as in the reference image
        compare_box = Rectangle(height=1.0, width=2.6, fill_color="#2C5F7C", fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
        compare_text = Text("Cosine-Similarity\nSearch", font_size=14, color=WHITE, font=CLEAN_FONT).move_to(compare_box)
        compare_group = VGroup(compare_box, compare_text)
        compare_group.next_to(aux_group, DOWN, buff=0.8)
        
        # Arrow from Aux Databases DOWN to Search box
        arrow_aux_to_search = Arrow(
            aux_group.get_bottom(), 
            compare_group.get_top(), 
            buff=0.1, 
            color=WHITE, 
            stroke_width=2, 
            max_tip_length_to_length_ratio=0.15
        )
        
        self.play(GrowArrow(arrow_aux_to_search), run_time=0.4)
        self.play(FadeIn(compare_group), run_time=0.4)
        
        # Arrow from E1 to Search box (horizontal from left)
        arrow_e1_to_search = Arrow(
            e1_group.get_right(), 
            compare_group.get_left(), 
            buff=0.1, 
            color=RED, 
            stroke_width=2, 
            max_tip_length_to_length_ratio=0.15
        )
        
        self.play(GrowArrow(arrow_e1_to_search), run_time=0.4)
        
        # Flash to show comparison happening
        self.play(Indicate(compare_group, color=YELLOW, scale_factor=1.05), run_time=0.4)
        
        # Animate comparison dots flowing
        for _ in range(2):
            dot = Dot(color=RED, radius=0.05).move_to(e1_group.get_right())
            self.play(dot.animate.move_to(compare_group.get_center()).set_opacity(0), run_time=0.25)
            self.remove(dot)

        # === TOP 10 CANDIDATES ===
        candidates_box = Rectangle(height=1.0, width=1.4, fill_color=GREY_E, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
        c_text = Text("Top 10\nPairs", font_size=14, color=WHITE, font=CLEAN_FONT).move_to(candidates_box)
        c_group = VGroup(candidates_box, c_text)
        c_group.next_to(compare_group, RIGHT, buff=0.6)
        
        arrow_to_candidates = Arrow(compare_group.get_right(), c_group.get_left(), buff=0.1, color=WHITE, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        self.play(GrowArrow(arrow_to_candidates), FadeIn(c_group), run_time=0.5)
        self.wait(1)

        # --- TRANSITION TO PHASE 3 (RE-RANKING) ---
        objects_to_fade = [
            header_2, trapezoid_group, input_group,
            bi_group_2, arrow_input, arrow_to_e1,
            e1_group, arrow_aux_to_search, arrow_e1_to_search,
            compare_group, arrow_to_candidates,
            aux_group, lbl_aux
        ]
        
        self.play(*[FadeOut(obj) for obj in objects_to_fade])
        
        # --- PHASE 3: RERANKING ---
        header_3 = Text("3. Re-Ranking Module", font_size=28, color=BLUE, font=CLEAN_FONT).to_edge(UP, buff=0.4)
        self.play(FadeIn(header_3), run_time=0.5)
        
        # === ORIGINAL ADDRESS AT TOP CENTER (matching image layout) ===
        original_address_text = "Rua Pinheiro Manso, Nº10, 3001-234"
        original_label = Text(original_address_text, font_size=18, color=WHITE, font=CLEAN_FONT)
        original_label.move_to(UP * 2.0)
        
        self.play(FadeIn(original_label, shift=DOWN * 0.2), run_time=0.5)
        self.wait(0.3)
        
        # === LAYOUT MATCHING THE IMAGE ===
        # Top-10 Pairs box on the LEFT
        # Trapezoid connector pointing to table on the RIGHT
        
        # Move the Top-10 Pairs box to the left side
        top10_box_pos = LEFT * 4.0 + DOWN * 0.3
        self.play(c_group.animate.move_to(top10_box_pos), run_time=0.5)
        
        # === CREATE TRAPEZOID CONNECTOR (pointing right toward table) ===
        # Trapezoid with wider end on right (toward table)
        trap_points = [
            [-0.8, 0.35, 0],   # Top-left (narrower, near Top-10 box)
            [0.8, 0.5, 0],    # Top-right (wider, toward table)
            [0.8, -0.5, 0],   # Bottom-right
            [-0.8, -0.35, 0], # Bottom-left
        ]
        trapezoid_connector = Polygon(*trap_points, fill_color="#2C5F7C", fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
        trapezoid_connector.next_to(c_group, RIGHT, buff=0.1)
        
        self.play(FadeIn(trapezoid_connector, shift=RIGHT * 0.2), run_time=0.4)
        
        # === CREATE TABLE WITH ADDRESSES (matching image format) ===
        # Show first 2 addresses, then "..." rows, then last 2 addresses
        candidate_row_height = 0.4
        candidate_row_width = 3.8
        
        # Addresses in initial order (unsorted, before reranking)
        # The correct match "Rua Pinheiro Manso, Nº10" will be at index 6
        initial_addresses = [
            ("R Pinheiro Manso, N1", 0.75),        # Medium match
            ("R Pinheiro Manso, N10", 0.88),       # Good match
            ("...", None),                         # Placeholder
            ("...", None),                         # Placeholder
            ("...", None),                         # Placeholder
            ("...", None),                         # Placeholder
            ("Rua Pinheiro Manso, Nº10", 0.98),   # BEST match (correct)
            ("R Pinheiro Bravo, LT4", 0.45),      # Poor match
            ("R dos Pinheiros, 23, xxxx-yyy", 0.32), # Worst match
        ]
        
        # Helper to create candidate row
        def create_table_row(addr, idx):
            fill_color = WHITE if idx % 2 == 0 else "#E8E8E8"
            row_bg = Rectangle(
                height=candidate_row_height, width=candidate_row_width,
                fill_color=fill_color, fill_opacity=1, 
                stroke_color="#AAAAAA", stroke_width=0.5
            )
            row_text = Text(addr, font_size=13, color=BLACK, font=CLEAN_FONT).move_to(row_bg)
            return VGroup(row_bg, row_text)
        
        # Table header
        table_header_bg = Rectangle(
            height=candidate_row_height + 0.05, width=candidate_row_width,
            fill_color="#2C5F7C", fill_opacity=1, stroke_color=WHITE, stroke_width=1
        )
        table_header_text = Text("Candidate Addresses", font_size=12, color=WHITE, font=CLEAN_FONT).move_to(table_header_bg)
        table_header = VGroup(table_header_bg, table_header_text)
        table_header.next_to(trapezoid_connector, RIGHT, buff=0)
        
        self.play(FadeIn(table_header, shift=RIGHT * 0.15), run_time=0.3)
        
        # Create and animate rows appearing one by one
        # Use separate dictionaries to track scores and addresses
        candidate_rows = VGroup()
        row_scores = {}  # index -> score
        row_addresses = {}  # index -> address
        
        for i, (addr, score) in enumerate(initial_addresses):
            row = create_table_row(addr, i)
            
            if i == 0:
                row.next_to(table_header, DOWN, buff=0)
            else:
                row.next_to(candidate_rows[-1], DOWN, buff=0)
            
            candidate_rows.add(row)
            row_scores[i] = score
            row_addresses[i] = addr
            
            # Animate each row appearing
            self.play(FadeIn(row, shift=DOWN * 0.12), run_time=0.15)
        
        self.wait(0.5)
        
        # Group the table parts
        table_group = VGroup(table_header, candidate_rows)
        
        # === RERANKING ANIMATION WITH SHUFFLING ===
        # Flash effect on table to indicate processing
        self.play(Indicate(table_group, color=YELLOW, scale_factor=1.02), run_time=0.4)
        
        # Get rows that have scores (not "..." placeholders)
        scored_rows = [(i, candidate_rows[i]) for i in range(len(candidate_rows)) if row_scores[i] is not None]
        
        # Sort by score (highest first = best match)
        sorted_scored = sorted(scored_rows, key=lambda x: row_scores[x[0]], reverse=True)
        
        # Create target positions (the positions after reranking)
        # Best match goes to top, worst to bottom
        row_positions = [row.get_center() for row in candidate_rows]
        
        # Perform the shuffle animation in stages
        # Stage 1: All scored rows glow briefly
        glow_anims = []
        for i, row in scored_rows:
            glow_anims.append(Indicate(row, color=BLUE_B, scale_factor=1.03))
        self.play(*glow_anims, run_time=0.4)
        
        # Stage 2: Shuffle animation - rows swap positions
        # We'll animate them moving to intermediate chaotic positions, then to final sorted positions
        
        # First, create a "chaos" shuffle - move rows randomly
        import random
        random.seed(42)  # Reproducible randomness
        
        shuffle_positions = row_positions.copy()
        random.shuffle(shuffle_positions)
        
        # Animate chaos shuffle
        chaos_anims = []
        for idx, (orig_i, row) in enumerate(scored_rows):
            # Move to a shuffled position
            target_pos = shuffle_positions[idx % len(shuffle_positions)]
            chaos_anims.append(row.animate.move_to(target_pos))
        self.play(*chaos_anims, run_time=0.5)
        
        # Stage 3: Sort animation - rows move to their final sorted positions
        # The best match (highest score) goes to position 0, etc.
        
        sort_anims = []
        for new_idx, (orig_i, row) in enumerate(sorted_scored):
            # Move to the position that corresponds to this rank
            target_pos = row_positions[new_idx]
            sort_anims.append(row.animate.move_to(target_pos))
        
        self.play(*sort_anims, run_time=0.6)
        
        # Brief pause to show sorted state
        self.wait(0.3)
        
        # === HIGHLIGHT THE TOP ROW (BEST MATCH) ===
        best_match_idx = sorted_scored[0][0]  # Original index of best match
        best_match_row = sorted_scored[0][1]  # First in sorted order = best match
        best_match_address = row_addresses[best_match_idx]
        
        # Create highlight border
        highlight_rect = Rectangle(
            height=candidate_row_height + 0.1, width=candidate_row_width + 0.1,
            stroke_color="#4CAF50", stroke_width=4, fill_opacity=0
        ).move_to(best_match_row)
        
        self.play(Create(highlight_rect), run_time=0.4)
        
        # Change the row to green styling
        best_match_new_bg = Rectangle(
            height=candidate_row_height, width=candidate_row_width,
            fill_color="#2a6b3a", fill_opacity=1, 
            stroke_color="#4CAF50", stroke_width=2
        ).move_to(best_match_row)
        best_match_new_text = Text(best_match_address, font_size=13, color=WHITE, font=CLEAN_FONT).move_to(best_match_new_bg)
        best_match_styled = VGroup(best_match_new_bg, best_match_new_text)
        
        # Track which rows to fade out BEFORE the transform (exclude best_match_row)
        rows_to_fade = [candidate_rows[i] for i in range(len(candidate_rows)) if i != best_match_idx]
        
        self.play(
            ReplacementTransform(best_match_row, best_match_styled),
            run_time=0.4
        )
        
        self.play(Indicate(best_match_styled, color=GREEN, scale_factor=1.05), run_time=0.4)
        
        # Add "Best Match" label
        best_label = Text("← Best Match (98%)", font_size=14, color="#4CAF50", font=CLEAN_FONT)
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
        match_label = Text("Matched Address", font_size=16, color="#4CAF50", font=CLEAN_FONT)
        match_label.next_to(best_match_styled, UP, buff=0.2)
        self.play(FadeIn(match_label), run_time=0.3)
        
        # === COMPARISON ANIMATION ===
        # Draw comparison arrow between original and match
        comparison_arrow = DoubleArrow(
            original_label.get_bottom(), 
            match_label.get_top(), 
            buff=0.15, 
            color=GREEN, 
            stroke_width=3,
            max_tip_length_to_length_ratio=0.08
        )
        
        self.play(GrowArrow(comparison_arrow), run_time=0.5)
        
        # Highlight matching parts with a glow effect
        comparison_label = Text("✓ Matched!", font_size=22, color="#4CAF50", font=CLEAN_FONT)
        comparison_label.next_to(comparison_arrow, RIGHT, buff=0.4)
        
        self.play(FadeIn(comparison_label, scale=1.2), run_time=0.4)
        
        # Final flash on both addresses
        self.play(
            Indicate(original_label, color=GREEN, scale_factor=1.05),
            Indicate(best_match_styled, color=GREEN, scale_factor=1.05),
            run_time=0.5
        )
        
        # === FINAL RESULT BOX ===
        final_box = Rectangle(height=1.0, width=2.8, fill_color="#1a4a1a", fill_opacity=0.9, stroke_color="#4CAF50", stroke_width=3)
        final_text = VGroup(
            Text("Door Accuracy", font_size=14, color=WHITE, font=CLEAN_FONT),
            Text("95.3%", font_size=28, color="#4CAF50", weight=BOLD, font=CLEAN_FONT)
        ).arrange(DOWN, buff=0.1).move_to(final_box)
        final_group = VGroup(final_box, final_text)
        final_group.next_to(best_match_styled, DOWN, buff=1.0)
        
        self.play(FadeIn(final_group, scale=0.8), run_time=0.5)
        self.play(Indicate(final_group, color=GREEN, scale_factor=1.08), run_time=0.5)
        
        self.wait(2)